from typing import Literal

from pydantic import BaseModel, Field


class ResultadoDiagnostico(BaseModel):

    evaluacion_general: str = Field(
        description=(
            "Resumen breve de la situación general del vehículo."
        )
    )

    sistema_relacionado: str = Field(
        description=(
            "Sistema principal del vehículo relacionado con los síntomas."
        )
    )

    nivel_riesgo: Literal[
        "bajo",
        "medio",
        "alto"
    ] = Field(
        description=(
            "Nivel general de riesgo determinado "
            "a partir de los análisis disponibles."
        )
    )

    causas_posibles: list[str] = Field(
        description=(
            "Lista de posibles causas. "
            "No deben presentarse como diagnósticos confirmados."
        )
    )

    evidencia_tecnica: str = Field(
        description=(
            "Resumen de la información relevante "
            "recuperada mediante RAG."
        )
    )

    fuente_tecnica: str = Field(
        description=(
            "Fuente indicada por el sistema RAG. "
            "Si no existe, usar 'No disponible'."
        )
    )

    evaluacion_seguridad: str = Field(
        description=(
            "Evaluación breve realizada por el agente de seguridad."
        )
    )

    seguridad_conduccion: Literal[
        "seguro",
        "precaucion",
        "no_recomendado"
    ] = Field(
        description=(
            "Indica si es seguro conducir, "
            "si requiere precaución o si no se recomienda conducir."
        )
    )

    requiere_revision_profesional: bool = Field(
        description=(
            "Indica si corresponde recomendar una revisión profesional."
        )
    )

    recomendaciones: list[str] = Field(
        description=(
            "Lista breve de acciones recomendadas."
        )
    )

    advertencia: str = Field(
        description=(
            "Advertencia sobre incertidumbre o necesidad "
            "de inspección física."
        )
    )