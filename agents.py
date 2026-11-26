from crewai import Agent
from services.agent_observability import iteration_limit_callback

from llm_config import (
    crear_llm,
    crear_llm_json
)

from tools.diagnosis import (
    diagnosticar_sintoma
)

from tools.maintenance import (
    consultar_mantenimiento
)

from tools.knowledge_search import (
    buscar_conocimiento_tecnico
)


# =========================================================
# AGENTE MECÁNICO
# =========================================================

def crear_agente_mecanico():

    return Agent(

        role=(
            "Especialista en Diagnóstico Automotriz"
        ),

        goal=(
            "Analizar síntomas automotrices de manera segura "
            "e identificar posibles causas y sistemas relacionados."
        ),

        backstory=(
            "Eres un especialista en diagnóstico automotriz. "
            "Analizas síntomas mecánicos y eléctricos con precaución. "
            "Cuando exista información en tus herramientas debes "
            "consultarla antes de elaborar una conclusión. "
            "No afirmas diagnósticos definitivos sin evidencia."
        ),

        tools=[
            diagnosticar_sintoma,
            consultar_mantenimiento
        ],

        llm=crear_llm(
    max_tokens=250
),

        verbose=False,

        allow_delegation=False,

        max_iter=5,
        max_execution_time=120,
        step_callback=iteration_limit_callback("mechanic", 5),
    )


# =========================================================
# AGENTE INVESTIGADOR
# =========================================================

def crear_agente_investigador():

    return Agent(

        role=(
            "Investigador Técnico Automotriz"
        ),

        goal=(
            "Buscar información técnica relevante que respalde "
            "el análisis de problemas automotrices."
        ),

        backstory=(
            "Eres un investigador especializado en documentación "
            "técnica automotriz. "
            "Tu función principal es consultar la base de conocimiento "
            "de AutoDiag AI mediante RAG. "
            "No debes inventar información que no esté respaldada "
            "por los documentos recuperados."
        ),

        tools=[
            buscar_conocimiento_tecnico
        ],

        llm=crear_llm(
    max_tokens=200
),

        verbose=False,

        allow_delegation=False,

        max_iter=5,
        max_execution_time=120,
        step_callback=iteration_limit_callback("researcher", 5),
    )


# =========================================================
# AGENTE SEGURIDAD
# =========================================================

def crear_agente_seguridad():

    return Agent(

        role=(
            "Revisor de Seguridad Automotriz"
        ),

        goal=(
            "Evaluar el nivel de riesgo asociado a un problema "
            "automotriz y determinar las advertencias necesarias."
        ),

        backstory=(
            "Eres responsable exclusivamente de revisar la seguridad. "
            "Analizas el resultado del especialista mecánico y detectas "
            "situaciones que puedan representar peligro. "
            "No inventas nuevas causas. "
            "Si existe evidencia de riesgo alto, no debes reducirlo "
            "sin evidencia clara."
        ),

        llm=crear_llm(
    max_tokens=180
),

        verbose=False,

        allow_delegation=False,

        max_iter=5,
        max_execution_time=120,
        step_callback=iteration_limit_callback("safety_reviewer", 5),
    )


# =========================================================
# AGENTE SINTETIZADOR
# =========================================================

def crear_agente_sintetizador():

    return Agent(

        role=(
            "Especialista en Síntesis Diagnóstica"
        ),

        goal=(
            "Integrar el análisis mecánico, la información técnica "
            "y la evaluación de seguridad en una respuesta final "
            "estructurada y clara."
        ),

        backstory=(
            "Eres responsable de producir la evaluación final "
            "de AutoDiag AI. "
            "Debes combinar únicamente información producida por "
            "los otros especialistas. "
            "No inventes información ni presentes hipótesis "
            "como diagnósticos definitivos. "
            "Tu respuesta final debe respetar estrictamente "
            "el formato JSON solicitado."
        ),

        llm=crear_llm_json(
            max_tokens=500
        ),

        verbose=False,

        allow_delegation=False,

        max_iter=3,
        max_execution_time=120,
        step_callback=iteration_limit_callback("synthesizer", 3),
    )
