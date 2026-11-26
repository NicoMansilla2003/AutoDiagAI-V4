"""Per-account limits for expensive diagnostic requests."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from services.history import obtener_conexion

DEFAULT_MAX_INPUT_CHARS = 4000


class RequestRateLimited(ValueError):
    """The account has reached its diagnostic request allowance."""


def max_input_chars() -> int:
    try:
        return max(500, min(int(os.getenv("AUTODIAG_MAX_INPUT_CHARS", DEFAULT_MAX_INPUT_CHARS)), 12000))
    except ValueError:
        return DEFAULT_MAX_INPUT_CHARS


def validate_input_length(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Describe al menos un síntoma.")
    limit = max_input_chars()
    if len(value) > limit:
        raise ValueError(f"La consulta supera el máximo de {limit} caracteres.")


def consume_diagnostic_request(user_id: int) -> None:
    """Allow a configurable number of diagnostic starts per user per minute."""
    try:
        limit = max(1, min(int(os.getenv("AUTODIAG_REQUESTS_PER_MINUTE", "5")), 100))
    except ValueError:
        limit = 5
    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(minutes=1)).isoformat()
    with obtener_conexion() as conn:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS diagnostic_requests (
                   user_id INTEGER NOT NULL,
                   requested_at TEXT NOT NULL
               )"""
        )
        conn.execute("DELETE FROM diagnostic_requests WHERE requested_at < ?", (cutoff,))
        count = conn.execute(
            "SELECT COUNT(*) FROM diagnostic_requests WHERE user_id=? AND requested_at>=?",
            (user_id, cutoff),
        ).fetchone()[0]
        if count >= limit:
            raise RequestRateLimited("Has alcanzado el límite temporal de diagnósticos. Espera un minuto.")
        conn.execute(
            "INSERT INTO diagnostic_requests(user_id,requested_at) VALUES(?,?)",
            (user_id, now.isoformat()),
        )
