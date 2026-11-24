import base64
import os

from email.message import EmailMessage
from html import escape
from pathlib import Path

from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# =========================================================
# VARIABLES DE ENTORNO
# =========================================================

load_dotenv()


# =========================================================
# RUTAS
# =========================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

SECRETS_DIR = (
    BASE_DIR
    / "secrets"
)

CREDENTIALS_PATH = (
    SECRETS_DIR
    / "gmail_credentials.json"
)

TOKEN_PATH = (
    SECRETS_DIR
    / "gmail_token.json"
)


# =========================================================
# PERMISOS
# =========================================================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]


# =========================================================
# CORREO CONFIGURADO
# =========================================================

AUTODIAG_EMAIL = (
    os.getenv(
        "AUTODIAG_EMAIL",
        ""
    )
    .strip()
)


# =========================================================
# CORREO DESTINO
# =========================================================

def obtener_correo_destino() -> str:

    if not AUTODIAG_EMAIL:

        raise ValueError(
            "No se encontró AUTODIAG_EMAIL "
            "en el archivo .env."
        )

    if "@" not in AUTODIAG_EMAIL:

        raise ValueError(
            "AUTODIAG_EMAIL no parece ser "
            "una dirección válida."
        )

    return AUTODIAG_EMAIL


# =========================================================
# CREDENCIALES OAUTH
# =========================================================

def obtener_credenciales() -> Credentials:

    SECRETS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    credenciales = None


    # =====================================================
    # TOKEN EXISTENTE
    # =====================================================

    if TOKEN_PATH.exists():

        try:

            credenciales = (
                Credentials
                .from_authorized_user_file(
                    str(TOKEN_PATH),
                    SCOPES
                )
            )

        except Exception as error:

            raise RuntimeError(
                "No fue posible leer gmail_token.json. "
                "Si modificaste los permisos OAuth, elimina "
                "el archivo gmail_token.json y vuelve a autenticar."
            ) from error


    # =====================================================
    # TOKEN NO VÁLIDO
    # =====================================================

    if (
        not credenciales
        or not credenciales.valid
    ):

        if (
            credenciales
            and credenciales.expired
            and credenciales.refresh_token
        ):

            try:

                credenciales.refresh(
                    Request()
                )

            except Exception as error:

                raise RuntimeError(
                    "No fue posible renovar "
                    "la sesión de Gmail."
                ) from error


        else:

            if not CREDENTIALS_PATH.exists():

                raise FileNotFoundError(
                    "No se encontró "
                    "secrets/gmail_credentials.json."
                )


            try:

                flow = (
                    InstalledAppFlow
                    .from_client_secrets_file(
                        str(
                            CREDENTIALS_PATH
                        ),
                        SCOPES
                    )
                )

                credenciales = (
                    flow.run_local_server(
                        port=0,
                        open_browser=True
                    )
                )

            except Exception as error:

                raise RuntimeError(
                    "No fue posible completar "
                    "la autenticación con Google."
                ) from error


        TOKEN_PATH.write_text(
            credenciales.to_json(),
            encoding="utf-8"
        )


    return credenciales


# =========================================================
# SERVICIO GMAIL
# =========================================================

def obtener_servicio_gmail():

    credenciales = (
        obtener_credenciales()
    )

    return build(
        "gmail",
        "v1",
        credentials=credenciales,
        cache_discovery=False
    )


# =========================================================
# TEXTO SEGURO
# =========================================================

def valor_texto(
    valor,
    defecto="No especificado"
) -> str:

    if valor is None:

        return defecto

    texto = str(valor).strip()

    if not texto:

        return defecto

    return texto


# =========================================================
# INFORME EN TEXTO
# =========================================================

def crear_texto_informe(
    resultado: dict,
    vehiculo: dict,
    sintoma: str
) -> str:

    causas = "\n".join(
        f"- {causa}"
        for causa
        in resultado.get(
            "causas_posibles",
            []
        )
    )

    recomendaciones = "\n".join(
        f"- {recomendacion}"
        for recomendacion
        in resultado.get(
            "recomendaciones",
            []
        )
    )

    revision = (
        "Sí"
        if resultado.get(
            "requiere_revision_profesional",
            False
        )
        else "No"
    )


    return f"""
AUTODIAG AI V3
INFORME DE DIAGNÓSTICO AUTOMOTRIZ


DATOS DEL VEHÍCULO

Marca:
{valor_texto(vehiculo.get("marca"))}

Modelo:
{valor_texto(vehiculo.get("modelo"))}

Año:
{valor_texto(vehiculo.get("anio"))}

Motor:
{valor_texto(vehiculo.get("motor"))}

Kilometraje:
{valor_texto(vehiculo.get("kilometraje"))}


SÍNTOMA REPORTADO

{valor_texto(sintoma)}


EVALUACIÓN GENERAL

{valor_texto(
    resultado.get("evaluacion_general"),
    "No disponible"
)}


SISTEMA RELACIONADO

{valor_texto(
    resultado.get("sistema_relacionado"),
    "No determinado"
)}


NIVEL DE RIESGO

{valor_texto(
    resultado.get("nivel_riesgo"),
    "No determinado"
).upper()}


POSIBLES CAUSAS

{causas or "- No disponibles"}


CONOCIMIENTO TÉCNICO

{valor_texto(
    resultado.get("evidencia_tecnica"),
    "No disponible"
)}


FUENTE TÉCNICA

{valor_texto(
    resultado.get("fuente_tecnica"),
    "No disponible"
)}


EVALUACIÓN DE SEGURIDAD

{valor_texto(
    resultado.get("evaluacion_seguridad"),
    "No disponible"
)}


SEGURIDAD DE CONDUCCIÓN

{valor_texto(
    resultado.get("seguridad_conduccion"),
    "No determinado"
)}


REQUIERE REVISIÓN PROFESIONAL

{revision}


ACCIONES RECOMENDADAS

{recomendaciones or "- No disponibles"}


LIMITACIONES DEL DIAGNÓSTICO

{valor_texto(
    resultado.get("advertencia"),
    "No disponible"
)}


------------------------------------------------------------

AutoDiag AI entrega información orientativa.

Este informe no reemplaza una inspección,
diagnóstico o reparación realizada por un profesional.
""".strip()


# =========================================================
# INFORME HTML
# =========================================================

def crear_html_informe(
    resultado: dict,
    vehiculo: dict,
    sintoma: str
) -> str:

    causas = resultado.get(
        "causas_posibles",
        []
    )

    recomendaciones = resultado.get(
        "recomendaciones",
        []
    )


    causas_html = "".join(
        f"""
        <li style="margin-bottom:8px;">
            {escape(str(causa))}
        </li>
        """
        for causa in causas
    )

    if not causas_html:

        causas_html = (
            "<li>No disponibles</li>"
        )


    recomendaciones_html = "".join(
        f"""
        <li style="margin-bottom:8px;">
            {escape(str(recomendacion))}
        </li>
        """
        for recomendacion
        in recomendaciones
    )

    if not recomendaciones_html:

        recomendaciones_html = (
            "<li>No disponibles</li>"
        )


    marca = escape(
        valor_texto(
            vehiculo.get("marca")
        )
    )

    modelo = escape(
        valor_texto(
            vehiculo.get("modelo")
        )
    )

    anio = escape(
        valor_texto(
            vehiculo.get("anio")
        )
    )

    motor = escape(
        valor_texto(
            vehiculo.get("motor")
        )
    )

    kilometraje = escape(
        valor_texto(
            vehiculo.get("kilometraje")
        )
    )

    sintoma_seguro = escape(
        valor_texto(
            sintoma
        )
    )

    evaluacion = escape(
        valor_texto(
            resultado.get(
                "evaluacion_general"
            ),
            "No disponible"
        )
    )

    sistema = escape(
        valor_texto(
            resultado.get(
                "sistema_relacionado"
            ),
            "No determinado"
        )
    )

    nivel = (
        valor_texto(
            resultado.get(
                "nivel_riesgo"
            ),
            "No determinado"
        )
        .lower()
    )

    evidencia = escape(
        valor_texto(
            resultado.get(
                "evidencia_tecnica"
            ),
            "No disponible"
        )
    )

    fuente = escape(
        valor_texto(
            resultado.get(
                "fuente_tecnica"
            ),
            "No disponible"
        )
    )

    seguridad = escape(
        valor_texto(
            resultado.get(
                "evaluacion_seguridad"
            ),
            "No disponible"
        )
    )

    conduccion = escape(
        valor_texto(
            resultado.get(
                "seguridad_conduccion"
            ),
            "No determinado"
        )
    )

    advertencia = escape(
        valor_texto(
            resultado.get(
                "advertencia"
            ),
            "No disponible"
        )
    )

    revision = (
        "Sí"
        if resultado.get(
            "requiere_revision_profesional",
            False
        )
        else "No"
    )


    colores = {
        "bajo": "#10B981",
        "medio": "#F59E0B",
        "alto": "#EF4444"
    }

    color_riesgo = colores.get(
        nivel,
        "#94A3B8"
    )


    return f"""
<!DOCTYPE html>

<html>

<head>
    <meta charset="UTF-8">
</head>

<body
    style="
        margin:0;
        padding:0;
        background:#0B0F17;
        color:#F8FAFC;
        font-family:Arial,Helvetica,sans-serif;
    "
>

<div
    style="
        max-width:720px;
        margin:0 auto;
        padding:32px 20px;
    "
>

    <div
        style="
            font-size:28px;
            font-weight:700;
            margin-bottom:4px;
        "
    >

        AutoDiag AI

        <span style="color:#3B82F6;">
            V3
        </span>

    </div>

    <div
        style="
            color:#64748B;
            font-size:12px;
            letter-spacing:1px;
            margin-bottom:28px;
        "
    >
        INFORME DE DIAGNÓSTICO AUTOMOTRIZ
    </div>


    <div style="
        background:#111827;
        border:1px solid #1E293B;
        border-radius:16px;
        padding:20px;
        margin-bottom:16px;
    ">

        <strong>
            🚗 Datos del vehículo
        </strong>

        <p style="
            color:#CBD5E1;
            line-height:1.8;
        ">

            <strong>Marca:</strong>
            {marca}

            <br>

            <strong>Modelo:</strong>
            {modelo}

            <br>

            <strong>Año:</strong>
            {anio}

            <br>

            <strong>Motor:</strong>
            {motor}

            <br>

            <strong>Kilometraje:</strong>
            {kilometraje}

        </p>

    </div>


    <div style="
        background:#111827;
        border:1px solid #1E293B;
        border-radius:16px;
        padding:20px;
        margin-bottom:16px;
    ">

        <strong>
            📝 Síntoma reportado
        </strong>

        <p style="
            color:#CBD5E1;
            line-height:1.7;
        ">
            {sintoma_seguro}
        </p>

    </div>


    <div style="
        background:#111827;
        border:1px solid #1E293B;
        border-radius:16px;
        padding:20px;
        margin-bottom:16px;
    ">

        <div style="
            color:#64748B;
            font-size:11px;
            font-weight:700;
            letter-spacing:1px;
        ">
            EVALUACIÓN DEL DIAGNÓSTICO
        </div>

        <h2 style="
            margin-top:7px;
            margin-bottom:12px;
        ">
            {sistema}
        </h2>


        <div style="
            display:inline-block;
            padding:6px 12px;
            border-radius:999px;
            background:{color_riesgo}22;
            border:1px solid {color_riesgo};
            color:{color_riesgo};
            font-size:12px;
            font-weight:700;
        ">
            RIESGO {escape(nivel.upper())}
        </div>


        <p style="
            color:#CBD5E1;
            line-height:1.7;
            margin-top:18px;
        ">
            {evaluacion}
        </p>

    </div>


    <div style="
        background:#111827;
        border:1px solid #1E293B;
        border-radius:16px;
        padding:20px;
        margin-bottom:16px;
    ">

        <strong>
            ⚙️ Posibles causas
        </strong>

        <ul style="
            color:#CBD5E1;
            line-height:1.7;
        ">
            {causas_html}
        </ul>

    </div>


    <div style="
        background:#111827;
        border:1px solid rgba(59,130,246,0.45);
        border-radius:16px;
        padding:20px;
        margin-bottom:16px;
    ">

        <strong>
            📚 Conocimiento técnico
        </strong>

        <div style="
            color:#3B82F6;
            font-size:11px;
            margin-top:8px;
            margin-bottom:14px;
        ">
            FUENTE / {fuente}
        </div>

        <div style="
            color:#CBD5E1;
            line-height:1.7;
        ">
            {evidencia}
        </div>

    </div>


    <div style="
        background:#111827;
        border:1px solid rgba(245,158,11,0.40);
        border-radius:16px;
        padding:20px;
        margin-bottom:16px;
    ">

        <strong>
            🛡️ Evaluación de seguridad
        </strong>

        <p style="
            color:#CBD5E1;
            line-height:1.7;
        ">
            {seguridad}
        </p>

        <div style="
            color:#94A3B8;
            line-height:1.8;
            font-size:13px;
        ">

            <strong>
                Seguridad de conducción:
            </strong>

            {conduccion}

            <br>

            <strong>
                Revisión profesional:
            </strong>

            {revision}

        </div>

    </div>


    <div style="
        background:#111827;
        border:1px solid #1E293B;
        border-radius:16px;
        padding:20px;
        margin-bottom:16px;
    ">

        <strong>
            ✅ Acciones recomendadas
        </strong>

        <ul style="
            color:#CBD5E1;
            line-height:1.7;
        ">
            {recomendaciones_html}
        </ul>

    </div>


    <div style="
        background:rgba(59,130,246,0.06);
        border:1px solid rgba(59,130,246,0.20);
        border-radius:12px;
        padding:16px;
        color:#94A3B8;
        font-size:12px;
        line-height:1.7;
    ">

        <strong>
            ℹ️ Limitaciones del diagnóstico
        </strong>

        <br><br>

        {advertencia}

        <br><br>

        AutoDiag AI entrega información orientativa
        y no sustituye una inspección profesional.

    </div>

</div>

</body>

</html>
"""


# =========================================================
# ENVIAR INFORME
# =========================================================

def enviar_informe_gmail(
    resultado: dict,
    vehiculo: dict,
    sintoma: str
) -> dict:

    destino = (
        obtener_correo_destino()
    )

    servicio = (
        obtener_servicio_gmail()
    )


    mensaje = EmailMessage()

    mensaje["To"] = destino

    mensaje["From"] = destino

    mensaje["Subject"] = (
        "AutoDiag AI V4 · Informe de diagnóstico"
    )


    mensaje.set_content(
        crear_texto_informe(
            resultado=resultado,
            vehiculo=vehiculo,
            sintoma=sintoma
        )
    )


    mensaje.add_alternative(
        crear_html_informe(
            resultado=resultado,
            vehiculo=vehiculo,
            sintoma=sintoma
        ),
        subtype="html"
    )


    mensaje_codificado = (
        base64
        .urlsafe_b64encode(
            mensaje.as_bytes()
        )
        .decode("utf-8")
    )


    try:

        respuesta = (
            servicio
            .users()
            .messages()
            .send(
                userId="me",
                body={
                    "raw":
                        mensaje_codificado
                }
            )
            .execute()
        )

    except HttpError as error:

        raise RuntimeError(
            "Gmail API rechazó el envío del informe."
        ) from error


    return {
        "id":
            respuesta.get(
                "id",
                ""
            ),

        "thread_id":
            respuesta.get(
                "threadId",
                ""
            ),

        "destino":
            destino
    }