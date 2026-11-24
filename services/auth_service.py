"""Own-account authentication and authorization primitives for AutoDiag AI V4."""

from __future__ import annotations

import argparse
import hashlib
import re
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from getpass import getpass

from argon2 import PasswordHasher, Type
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from services.history import inicializar_db, obtener_conexion

PASSWORD_HASHER = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2, type=Type.ID)
MAX_LOGIN_FAILURES = 5
LOGIN_WINDOW_MINUTES = 15
SESSION_TTL_HOURS = 12
_EMAIL_LOCAL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+$")


class AuthError(ValueError):
    """A safe, user-displayable authentication error."""


class RateLimited(AuthError):
    """Login attempts for this normalized address are temporarily blocked."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_email(email: str) -> str:
    if not isinstance(email, str):
        raise AuthError("Ingresa un correo válido.")
    value = email.strip()
    if len(value) > 254 or value.count("@") != 1:
        raise AuthError("Ingresa un correo válido.")
    local, domain = value.rsplit("@", 1)
    if (
        not local or len(local) > 64 or local.startswith(".") or local.endswith(".")
        or ".." in local or not _EMAIL_LOCAL_RE.fullmatch(local)
    ):
        raise AuthError("Ingresa un correo válido.")
    try:
        ascii_domain = domain.rstrip(".").encode("idna").decode("ascii").lower()
    except UnicodeError as error:
        raise AuthError("Ingresa un correo válido.") from error
    labels = ascii_domain.split(".")
    if len(labels) < 2 or any(
        not label or len(label) > 63 or label.startswith("-") or label.endswith("-")
        or not re.fullmatch(r"[a-z0-9-]+", label)
        for label in labels
    ):
        raise AuthError("Ingresa un correo válido.")
    return f"{local.casefold()}@{ascii_domain}"


def validate_password(password: str) -> None:
    if not isinstance(password, str) or not 12 <= len(password) <= 128:
        raise AuthError("La contraseña debe tener entre 12 y 128 caracteres.")


def initialize_auth_db() -> None:
    """Create authentication tables and add the nullable history owner column."""
    with obtener_conexion() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user' CHECK(role IN ('user','admin')),
                is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0,1)),
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS auth_sessions (
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                revoked_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_auth_sessions_user ON auth_sessions(user_id);
            CREATE TABLE IF NOT EXISTS auth_login_failures (
                email TEXT NOT NULL,
                attempted_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_auth_failures_email_time
                ON auth_login_failures(email, attempted_at);
            """
        )
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(diagnosticos)")}
        if "user_id" not in columns:
            conn.execute(
                "ALTER TABLE diagnosticos ADD COLUMN user_id INTEGER REFERENCES users(id)"
            )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_diagnosticos_user_id ON diagnosticos(user_id)"
        )


def _new_session(conn: sqlite3.Connection, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    now = utc_now()
    token_hash = hashlib.sha256(token.encode("ascii")).hexdigest()
    conn.execute(
        "INSERT INTO auth_sessions(token_hash,user_id,created_at,expires_at) VALUES(?,?,?,?)",
        (token_hash, user_id, now.isoformat(), (now + timedelta(hours=SESSION_TTL_HOURS)).isoformat()),
    )
    return token


def register_user(display_name: str, email: str, password: str, confirm_password: str) -> tuple[dict, str]:
    name = " ".join(display_name.strip().split()) if isinstance(display_name, str) else ""
    if not 1 <= len(name) <= 100:
        raise AuthError("Ingresa un nombre de entre 1 y 100 caracteres.")
    normalized = normalize_email(email)
    validate_password(password)
    if password != confirm_password:
        raise AuthError("Las contraseñas no coinciden.")
    hashed = PASSWORD_HASHER.hash(password)
    try:
        with obtener_conexion() as conn:
            cursor = conn.execute(
                "INSERT INTO users(display_name,email,password_hash,role,created_at) VALUES(?,?,?,'user',?)",
                (name, normalized, hashed, utc_now().isoformat()),
            )
            user_id = cursor.lastrowid
            token = _new_session(conn, user_id)
            conn.commit()
            return {"id": user_id, "display_name": name, "email": normalized, "role": "user"}, token
    except sqlite3.IntegrityError as error:
        raise AuthError("No fue posible crear la cuenta con esos datos.") from error


def login(email: str, password: str) -> tuple[dict, str]:
    normalized = normalize_email(email)
    if not isinstance(password, str) or len(password) > 1024:
        raise AuthError("Correo o contraseña incorrectos.")
    now = utc_now()
    cutoff = (now - timedelta(minutes=LOGIN_WINDOW_MINUTES)).isoformat()
    with obtener_conexion() as conn:
        conn.execute("DELETE FROM auth_login_failures WHERE attempted_at < ?", (cutoff,))
        count = conn.execute(
            "SELECT COUNT(*) FROM auth_login_failures WHERE email=? AND attempted_at>=?",
            (normalized, cutoff),
        ).fetchone()[0]
        if count >= MAX_LOGIN_FAILURES:
            raise RateLimited("Demasiados intentos. Espera 15 minutos antes de volver a intentar.")
        user = conn.execute(
            "SELECT id,display_name,email,password_hash,role,is_active FROM users WHERE email=?",
            (normalized,),
        ).fetchone()
        try:
            if user is None:
                # Similar-cost hashing avoids a fast response for unknown accounts.
                PASSWORD_HASHER.hash(password)
                raise VerifyMismatchError
            PASSWORD_HASHER.verify(user["password_hash"], password)
            if not user["is_active"]:
                raise VerifyMismatchError
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            conn.execute(
                "INSERT INTO auth_login_failures(email,attempted_at) VALUES(?,?)",
                (normalized, now.isoformat()),
            )
            conn.commit()
            raise AuthError("Correo o contraseña incorrectos.") from None
        conn.execute("DELETE FROM auth_login_failures WHERE email=?", (normalized,))
        token = _new_session(conn, user["id"])
        conn.commit()
        return {key: user[key] for key in ("id", "display_name", "email", "role")}, token


def resolve_session(token: str | None) -> dict | None:
    if not isinstance(token, str) or not token:
        return None
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = utc_now().isoformat()
    with obtener_conexion() as conn:
        row = conn.execute(
            """SELECT u.id,u.display_name,u.email,u.role
               FROM auth_sessions s JOIN users u ON u.id=s.user_id
               WHERE s.token_hash=? AND s.revoked_at IS NULL AND s.expires_at>? AND u.is_active=1""",
            (token_hash, now),
        ).fetchone()
    return dict(row) if row else None


def logout(token: str | None) -> None:
    if not isinstance(token, str) or not token:
        return
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with obtener_conexion() as conn:
        conn.execute(
            "UPDATE auth_sessions SET revoked_at=? WHERE token_hash=? AND revoked_at IS NULL",
            (utc_now().isoformat(), token_hash),
        )


def bootstrap_first_admin(email: str, password: str, display_name: str = "Administrador") -> None:
    """Create the first admin once; no public registration path can grant this role."""
    normalized = normalize_email(email)
    validate_password(password)
    hashed = PASSWORD_HASHER.hash(password)
    with obtener_conexion() as conn:
        conn.execute("BEGIN IMMEDIATE")
        if conn.execute("SELECT 1 FROM users WHERE role='admin' AND is_active=1 LIMIT 1").fetchone():
            raise AuthError("Ya existe un administrador activo.")
        try:
            conn.execute(
                "INSERT INTO users(display_name,email,password_hash,role,created_at) VALUES(?,?,?,'admin',?)",
                (display_name.strip()[:100] or "Administrador", normalized, hashed, utc_now().isoformat()),
            )
            conn.commit()
        except sqlite3.IntegrityError as error:
            raise AuthError("No fue posible crear el administrador con esos datos.") from error


def _bootstrap_cli() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap seguro del primer administrador de AutoDiag AI V4.")
    parser.add_argument("command", choices=["bootstrap-admin"])
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", default="Administrador")
    args = parser.parse_args()
    inicializar_db()
    initialize_auth_db()
    password = getpass("Contraseña nueva del administrador (mínimo 12 caracteres): ")
    confirmation = getpass("Confirma la contraseña: ")
    if password != confirmation:
        parser.error("Las contraseñas no coinciden.")
    bootstrap_first_admin(args.email, password, args.name)
    print("Administrador inicial creado.")


if __name__ == "__main__":
    _bootstrap_cli()
