import os

import crewai.llms.cache as crew_cache
from crewai.llm import LLM
from dotenv import load_dotenv


# =========================================================
# WORKAROUND CREWAI + GROQ
# =========================================================

crew_cache.mark_cache_breakpoint = lambda message: message


# =========================================================
# VARIABLES DE ENTORNO
# =========================================================

load_dotenv()


# =========================================================
# LLM GENERAL
# =========================================================

def crear_llm(
    max_tokens: int = 300,
    reasoning_effort: str = "low"
):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "No se encontró GROQ_API_KEY en el archivo .env"
        )

    return LLM(
        model="groq/openai/gpt-oss-120b",
        temperature=0,
        max_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
        timeout=60,
        max_retries=1
    )


# =========================================================
# LLM DEL SINTETIZADOR
# =========================================================

def crear_llm_json(
    max_tokens: int = 700,
    reasoning_effort: str = "low"
):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "No se encontró GROQ_API_KEY en el archivo .env"
        )

    return LLM(
        model="groq/openai/gpt-oss-120b",
        temperature=0,
        max_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
        timeout=60,
        max_retries=1,

        # Fuerza una respuesta JSON válida
        response_format={
            "type": "json_object"
        }
    )
