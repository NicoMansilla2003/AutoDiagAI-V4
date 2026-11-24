import json
import sqlite3

from contextlib import closing, contextmanager
from datetime import datetime
from pathlib import Path


# =========================================================
# RUTAS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "autodiag_history.db"


def _usuario_autorizado(session_token: str) -> dict:
    # Import locally to avoid a module cycle: auth uses this module's connection.
    from services.auth_service import resolve_session

    usuario = resolve_session(session_token)
    if usuario is None:
        raise PermissionError("Se requiere una sesión activa.")
    return usuario


# =========================================================
# CONEXIÓN
# =========================================================

@contextmanager
def obtener_conexion():
    """
    Crea una conexión nueva a SQLite.
    """

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conexion = sqlite3.connect(
        DB_PATH,
        timeout=10
    )

    conexion.row_factory = sqlite3.Row

    with closing(conexion):
        with conexion:
            yield conexion


# =========================================================
# INICIALIZAR BASE
# =========================================================

def inicializar_db():
    """
    Crea la tabla de diagnósticos si todavía no existe.
    """

    with obtener_conexion() as conexion:

        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS diagnosticos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                fecha TEXT NOT NULL,

                marca TEXT,
                modelo TEXT,
                anio TEXT,
                motor TEXT,
                kilometraje TEXT,

                consulta TEXT NOT NULL,

                sistema TEXT,
                riesgo TEXT,

                resultado_json TEXT NOT NULL
            )
            """
        )

        conexion.commit()


# =========================================================
# GUARDAR DIAGNÓSTICO
# =========================================================

def guardar_diagnostico(
    consulta: str,
    resultado: dict,
    marca: str = "",
    modelo: str = "",
    anio: str = "",
    motor: str = "",
    kilometraje: str = "",
    session_token: str | None = None
) -> int:
    """
    Guarda un diagnóstico estructurado.

    Retorna el ID generado.
    """

    usuario = _usuario_autorizado(session_token)

    fecha = datetime.now().isoformat(
        timespec="seconds"
    )

    resultado_json = json.dumps(
        resultado,
        ensure_ascii=False
    )

    sistema = resultado.get(
        "sistema_relacionado",
        ""
    )

    riesgo = resultado.get(
        "nivel_riesgo",
        ""
    )

    with obtener_conexion() as conexion:

        cursor = conexion.execute(
            """
            INSERT INTO diagnosticos (

                fecha,

                marca,
                modelo,
                anio,
                motor,
                kilometraje,

                consulta,

                sistema,
                riesgo,

                resultado_json,
                user_id

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                fecha,

                marca,
                modelo,
                anio,
                motor,
                kilometraje,

                consulta,

                sistema,
                riesgo,

                resultado_json,
                usuario["id"]
            )
        )

        conexion.commit()

        return cursor.lastrowid


# =========================================================
# LISTAR DIAGNÓSTICOS
# =========================================================

def listar_diagnosticos(
    session_token: str | None = None,
    limite: int = 100
) -> list[dict]:
    """
    Devuelve los diagnósticos más recientes.
    """

    usuario = _usuario_autorizado(session_token)

    with obtener_conexion() as conexion:

        if usuario["role"] == "admin":
            filas = conexion.execute(
            """
            SELECT

                id,
                fecha,

                marca,
                modelo,
                anio,

                consulta,

                sistema,
                riesgo

            FROM diagnosticos

            ORDER BY id DESC

            LIMIT ?
            """,
                (limite,)
            ).fetchall()
        else:
            filas = conexion.execute(
                """SELECT id, fecha, marca, modelo, anio, consulta, sistema, riesgo
                   FROM diagnosticos WHERE user_id = ? ORDER BY id DESC LIMIT ?""",
                (usuario["id"], limite),
            ).fetchall()

    return [
        dict(fila)
        for fila in filas
    ]


# =========================================================
# OBTENER DIAGNÓSTICO
# =========================================================

def obtener_diagnostico(
    diagnostico_id: int,
    session_token: str | None = None,
) -> dict | None:
    """
    Recupera un diagnóstico completo utilizando su ID.
    """

    usuario = _usuario_autorizado(session_token)

    with obtener_conexion() as conexion:

        if usuario["role"] == "admin":
            fila = conexion.execute(
            """
            SELECT *

            FROM diagnosticos

            WHERE id = ?
            """,
                (diagnostico_id,)
            ).fetchone()
        else:
            fila = conexion.execute(
                "SELECT * FROM diagnosticos WHERE id = ? AND user_id = ?",
                (diagnostico_id, usuario["id"]),
            ).fetchone()

    if fila is None:
        return None

    diagnostico = dict(
        fila
    )

    diagnostico["resultado"] = json.loads(
        diagnostico[
            "resultado_json"
        ]
    )

    return diagnostico
