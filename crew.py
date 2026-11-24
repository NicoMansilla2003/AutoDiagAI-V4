import json

from crewai import Crew, Process
from pydantic import ValidationError

from agents import (
    crear_agente_mecanico,
    crear_agente_investigador,
    crear_agente_seguridad,
    crear_agente_sintetizador
)

from models import (
    ResultadoDiagnostico
)

from services.domain_guard import (
    validar_consulta_automotriz
)

from services.safety_guard import (
    evaluar_seguridad_critica,
    crear_contexto_seguridad,
    aplicar_guardia_seguridad
)

from tasks import (
    crear_tarea_diagnostico,
    crear_tarea_investigacion,
    crear_tarea_seguridad,
    crear_tarea_sintesis
)


# =========================================================
# EXTRAER JSON
# =========================================================

def extraer_json(
    texto: str
) -> dict:
    """
    Convierte la respuesta final del sintetizador
    en un diccionario Python.

    Tolera bloques Markdown accidentales
    y texto adicional.
    """

    if not texto:

        raise ValueError(
            "El sintetizador devolvió "
            "una respuesta vacía."
        )


    texto = texto.strip()


    # =====================================================
    # ELIMINAR BLOQUE MARKDOWN
    # =====================================================

    if texto.startswith("```"):

        lineas = texto.splitlines()


        if lineas:

            lineas = lineas[
                1:
            ]


        if (
            lineas
            and lineas[-1].strip()
            == "```"
        ):

            lineas = lineas[
                :-1
            ]


        texto = "\n".join(
            lineas
        ).strip()


    # =====================================================
    # JSON DIRECTO
    # =====================================================

    try:

        return json.loads(
            texto
        )

    except json.JSONDecodeError:

        pass


    # =====================================================
    # EXTRAER OBJETO
    # =====================================================

    inicio = texto.find(
        "{"
    )


    fin = texto.rfind(
        "}"
    )


    if (
        inicio == -1
        or fin == -1
        or fin <= inicio
    ):

        vista_previa = texto[
            :1000
        ]


        raise ValueError(
            "El sintetizador no devolvió "
            "un objeto JSON completo.\n\n"
            "Salida recibida:\n"
            f"{vista_previa}"
        )


    posible_json = texto[
        inicio:
        fin + 1
    ]


    try:

        return json.loads(
            posible_json
        )

    except json.JSONDecodeError as error:

        vista_previa = posible_json[
            :1000
        ]


        raise ValueError(
            "El sintetizador devolvió un objeto "
            "parecido a JSON, pero su sintaxis "
            "no es válida.\n\n"
            "Salida recibida:\n"
            f"{vista_previa}"
        ) from error


# =========================================================
# EJECUTAR DIAGNÓSTICO
# =========================================================

def ejecutar_diagnostico(
    consulta: str
):

    # =====================================================
    # 1. GUARDRAIL DE DOMINIO
    # =====================================================

    validar_consulta_automotriz(
        consulta
    )


    # =====================================================
    # 2. SAFETY GUARD LOCAL
    # =====================================================

    evaluacion_critica = (
        evaluar_seguridad_critica(
            consulta
        )
    )


    contexto_seguridad = (
        crear_contexto_seguridad(
            evaluacion_critica
        )
    )


    consulta_agentes = (
        consulta
        + contexto_seguridad
    )


    # =====================================================
    # 3. CREAR AGENTES
    # =====================================================

    agente_mecanico = (
        crear_agente_mecanico()
    )


    agente_investigador = (
        crear_agente_investigador()
    )


    agente_seguridad = (
        crear_agente_seguridad()
    )


    agente_sintetizador = (
        crear_agente_sintetizador()
    )


    # =====================================================
    # 4. CREAR TAREAS
    # =====================================================

    tarea_diagnostico = (
        crear_tarea_diagnostico(
            agente_mecanico,
            consulta_agentes
        )
    )


    tarea_investigacion = (
        crear_tarea_investigacion(
            agente_investigador,
            consulta_agentes
        )
    )


    tarea_seguridad = (
        crear_tarea_seguridad(
            agente_seguridad,
            consulta_agentes,
            tarea_diagnostico
        )
    )


    tarea_sintesis = (
        crear_tarea_sintesis(
            agente_sintetizador,
            consulta_agentes,
            tarea_diagnostico,
            tarea_investigacion,
            tarea_seguridad
        )
    )


    # =====================================================
    # 5. CREW
    # =====================================================

    crew = Crew(

        agents=[
            agente_mecanico,
            agente_investigador,
            agente_seguridad,
            agente_sintetizador
        ],

        tasks=[
            tarea_diagnostico,
            tarea_investigacion,
            tarea_seguridad,
            tarea_sintesis
        ],

        process=Process.sequential,

        verbose=True
    )


    # =====================================================
    # 6. EJECUTAR
    # =====================================================

    resultado = (
        crew.kickoff()
    )


    texto_final = (
        resultado.raw
    )


    # =====================================================
    # 7. PARSEAR JSON
    # =====================================================

    datos = (
        extraer_json(
            texto_final
        )
    )


    # =====================================================
    # 8. VALIDACIÓN PYDANTIC
    # =====================================================

    try:

        diagnostico = (
            ResultadoDiagnostico
            .model_validate(
                datos
            )
        )

    except ValidationError as error:

        raise ValueError(
            "El sintetizador produjo JSON, "
            "pero el resultado no cumple "
            "la estructura esperada por AutoDiag AI."
        ) from error


    diagnostico_dict = (
        diagnostico.model_dump()
    )


    # =====================================================
    # 9. PROTECCIÓN FINAL DE SEGURIDAD
    # =====================================================

    diagnostico_dict = (
        aplicar_guardia_seguridad(
            diagnostico_dict,
            evaluacion_critica
        )
    )


    # =====================================================
    # 10. VALIDAR NUEVAMENTE
    # =====================================================

    try:

        diagnostico_final = (
            ResultadoDiagnostico
            .model_validate(
                diagnostico_dict
            )
        )

    except ValidationError as error:

        raise ValueError(
            "El resultado final no superó "
            "la validación de seguridad y estructura."
        ) from error


    return (
        diagnostico_final
        .model_dump()
    )