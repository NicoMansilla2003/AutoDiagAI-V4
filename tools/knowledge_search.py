from crewai.tools import tool

from rag.vectorstore import (
    buscar_conocimiento_vectorial
)


# =========================================================
# HERRAMIENTA RAG PARA CREWAI
# =========================================================

@tool("Buscar conocimiento técnico automotriz")
def buscar_conocimiento_tecnico(
    consulta: str
) -> str:
    """
    Busca información técnica automotriz en la base
    de conocimiento de AutoDiag AI utilizando RAG.

    Utiliza esta herramienta cuando necesites consultar
    información relacionada con fallas, síntomas,
    componentes, mantenimiento o funcionamiento
    de un vehículo.

    Los documentos recuperados sirven como evidencia
    técnica orientativa.

    No deben interpretarse automáticamente como
    un diagnóstico definitivo.
    """

    return buscar_conocimiento_vectorial(

        consulta=consulta,

        # Mantener bajo para no inflar el contexto
        # enviado posteriormente a Groq.
        cantidad=1
    )