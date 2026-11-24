import sqlite3
import tempfile
import unittest
from pathlib import Path

from services import history
from services.auth_service import (
    AuthError,
    RateLimited,
    bootstrap_first_admin,
    initialize_auth_db,
    login,
    logout,
    normalize_email,
    register_user,
    resolve_session,
)


class AuthTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        history.DB_PATH = Path(self.tempdir.name) / "auth-test.sqlite3"
        history.inicializar_db()
        initialize_auth_db()

    def tearDown(self):
        self.tempdir.cleanup()

    def register(self, email="one@example.com", password="Long enough pass 123!"):
        return register_user("Test User", email, password, password)

    def test_email_normalization_and_password_validation(self):
        self.assertEqual(normalize_email(" User@ExAmPle.com "), "user@example.com")
        with self.assertRaises(AuthError):
            register_user("X", "not-an-email", "Long enough pass 123!", "Long enough pass 123!")
        with self.assertRaises(AuthError):
            register_user("X", "x@example.com", "short", "short")
        with self.assertRaises(AuthError):
            register_user("X", "x@example.com", "Long enough pass 123!", "different password")

    def test_register_login_hashing_and_role(self):
        user, token = self.register()
        self.assertEqual(user["role"], "user")
        self.assertIsNotNone(resolve_session(token))
        with history.obtener_conexion() as conn:
            row = conn.execute("SELECT password_hash,role FROM users WHERE id=?", (user["id"],)).fetchone()
        self.assertTrue(row["password_hash"].startswith("$argon2id$"))
        self.assertNotEqual(row["password_hash"], "Long enough pass 123!")
        _, login_token = login("ONE@example.com", "Long enough pass 123!")
        self.assertIsNotNone(resolve_session(login_token))
        with self.assertRaises(AuthError):
            self.register(email="one@EXAMPLE.com")

    def test_login_rate_limit(self):
        self.register()
        for _ in range(5):
            with self.assertRaises(AuthError):
                login("one@example.com", "Wrong password 123!")
        with self.assertRaises(RateLimited):
            login("one@example.com", "Long enough pass 123!")

    def test_sessions_revoke_and_expire(self):
        user, token = self.register()
        logout(token)
        self.assertIsNone(resolve_session(token))
        _, expiring_token = login("one@example.com", "Long enough pass 123!")
        token_hash = __import__("hashlib").sha256(expiring_token.encode()).hexdigest()
        with history.obtener_conexion() as conn:
            conn.execute("UPDATE auth_sessions SET expires_at='2000-01-01T00:00:00+00:00' WHERE token_hash=?", (token_hash,))
        self.assertIsNone(resolve_session(expiring_token))

    def test_history_is_private_and_legacy_rows_are_admin_only(self):
        with history.obtener_conexion() as conn:
            conn.execute(
                "INSERT INTO diagnosticos(fecha,consulta,resultado_json) VALUES(?,?,?)",
                ("2025-01-01T00:00:00", "legacy personal request", "{}"),
            )
        initialize_auth_db()
        _, first_token = self.register("one@example.com")
        _, second_token = self.register("two@example.com")
        diagnostic_id = history.guardar_diagnostico(
            "first user's symptom", {"nivel_riesgo": "bajo"}, session_token=first_token
        )
        self.assertEqual([row["id"] for row in history.listar_diagnosticos(first_token)], [diagnostic_id])
        self.assertEqual(history.listar_diagnosticos(second_token), [])
        self.assertIsNone(history.obtener_diagnostico(diagnostic_id, second_token))
        with self.assertRaises(PermissionError):
            history.listar_diagnosticos("invalid-token")
        self.assertIsNone(history.obtener_diagnostico(1, first_token))
        bootstrap_first_admin("admin@example.com", "Admin secure password 123!")
        _, admin_token = login("admin@example.com", "Admin secure password 123!")
        self.assertEqual(len(history.listar_diagnosticos(admin_token)), 2)
        self.assertEqual(history.obtener_diagnostico(1, admin_token)["consulta"], "legacy personal request")

    def test_only_bootstrap_can_create_admin(self):
        user, _ = self.register()
        self.assertEqual(user["role"], "user")
        bootstrap_first_admin("admin@example.com", "Admin secure password 123!")
        with self.assertRaises(AuthError):
            bootstrap_first_admin("admin2@example.com", "Another admin password 123!")
        with history.obtener_conexion() as conn:
            roles = [row[0] for row in conn.execute("SELECT role FROM users ORDER BY id")]
        self.assertEqual(roles, ["user", "admin"])


if __name__ == "__main__":
    unittest.main()
