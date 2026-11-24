import re
import unicodedata
from copy import deepcopy


# =========================================================
# NORMALIZACIÓN
# =========================================================

def normalizar_texto(
    texto: str
) -> str:

    texto = str(
        texto
    ).lower().strip()


    texto = unicodedata.normalize(
        "NFD",
        texto
    )


    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(
            caracter
        ) != "Mn"
    )


    texto = re.sub(
        r"[^a-z0-9\s]",
        " ",
        texto
    )


    texto = re.sub(
        r"\s+",
        " ",
        texto
    )


    return texto.strip()


# =========================================================
# EXTRAER SÍNTOMAS
# =========================================================

def extraer_sintomas(
    consulta: str
) -> str:

    consulta = str(
        consulta
    )


    patron = re.compile(
        r"s[ií]ntomas\s+reportados\s*:\s*(.*)",
        re.IGNORECASE | re.DOTALL
    )


    coincidencia = patron.search(
        consulta
    )


    if coincidencia:

        sintomas = (
            coincidencia
            .group(1)
            .strip()
        )


        if sintomas:

            return sintomas


    return consulta.strip()


# =========================================================
# ALERTAS CRÍTICAS
# =========================================================

ALERTAS_CRITICAS = [

    # =====================================================
    # FRENOS
    # =====================================================

    {
        "codigo":
            "FRENOS_CRITICOS",

        "titulo":
            "Posible pérdida de capacidad de frenado",

        "patrones": [
            r"\bsin frenos\b",
            r"\bno frena\b",
            r"\bno frena nada\b",
            r"\bperdi los frenos\b",
            r"\bperdio los frenos\b",
            r"\bme quede sin frenos\b",
            r"\bpedal de freno se va al fondo\b",
            r"\bpedal se va al fondo\b",
            r"\bfuga de liquido de frenos\b",
            r"\bpierde liquido de frenos\b"
        ],

        "mensaje":
            (
                "Se detectó una descripción compatible con una "
                "posible falla crítica del sistema de frenos."
            ),

        "recomendaciones": [
            "No continuar conduciendo el vehículo si la capacidad de frenado está comprometida.",
            "Detener el vehículo en un lugar seguro cuando sea posible.",
            "Solicitar una inspección profesional del sistema de frenos antes de volver a utilizarlo."
        ]
    },


    # =====================================================
    # PRESIÓN DE ACEITE
    # =====================================================

    {
        "codigo":
            "PRESION_ACEITE",

        "titulo":
            "Posible problema crítico de presión de aceite",

        "patrones": [
            r"\bpresion de aceite baja\b",
            r"\bsin presion de aceite\b",
            r"\bpresion de aceite cero\b",
            r"\btestigo de presion de aceite\b",
            r"\bluz roja de aceite\b",
            r"\btestigo rojo de aceite\b"
        ],

        "mensaje":
            (
                "Se detectó una posible advertencia relacionada "
                "con la presión de lubricación del motor."
            ),

        "recomendaciones": [
            "Evitar continuar utilizando el motor si existe una advertencia real de presión de aceite.",
            "Detener el motor de forma segura cuando corresponda.",
            "Solicitar revisión del nivel, presión y sistema de lubricación antes de continuar el uso normal."
        ]
    },


    # =====================================================
    # SOBRECALENTAMIENTO
    # =====================================================

    {
        "codigo":
            "SOBRECALENTAMIENTO",

        "titulo":
            "Posible sobrecalentamiento severo",

        "patrones": [
            r"\bsobrecalentamiento\b",
            r"\btemperatura al maximo\b",
            r"\btemperatura en rojo\b",
            r"\baguja de temperatura al maximo\b",
            r"\bsale vapor del motor\b",
            r"\bsale vapor del capot\b",
            r"\bmotor hirviendo\b"
        ],

        "mensaje":
            (
                "Se detectó una posible situación de "
                "sobrecalentamiento del motor."
            ),

        "recomendaciones": [
            "Detener el vehículo de forma segura si la temperatura está en una zona crítica.",
            "No abrir inmediatamente el sistema de refrigeración mientras esté caliente o presurizado.",
            "Revisar el sistema de refrigeración antes de continuar la conducción normal."
        ]
    },


    # =====================================================
    # DIRECCIÓN
    # =====================================================

    {
        "codigo":
            "DIRECCION_CRITICA",

        "titulo":
            "Posible pérdida de control de la dirección",

        "patrones": [
            r"\bperdi la direccion\b",
            r"\bperdio la direccion\b",
            r"\bdireccion no responde\b",
            r"\bdireccion se trabo\b",
            r"\bvolante se trabo\b",
            r"\bvolante bloqueado mientras conduzco\b"
        ],

        "mensaje":
            (
                "Se detectó una descripción compatible con una "
                "posible falla importante de la dirección."
            ),

        "recomendaciones": [
            "Evitar continuar conduciendo si el control de la dirección está comprometido.",
            "Detener el vehículo en un lugar seguro cuando sea posible.",
            "Solicitar una inspección profesional del sistema de dirección."
        ]
    },


    # =====================================================
    # COMBUSTIBLE
    # =====================================================

    {
        "codigo":
            "FUGA_COMBUSTIBLE",

        "titulo":
            "Posible fuga de combustible",

        "patrones": [
            r"\bfuga de gasolina\b",
            r"\bfuga de bencina\b",
            r"\bpierde gasolina\b",
            r"\bpierde bencina\b",
            r"\bgotea gasolina\b",
            r"\bgotea bencina\b",
            r"\bolor fuerte a gasolina dentro\b",
            r"\bolor fuerte a bencina dentro\b"
        ],

        "mensaje":
            (
                "Se detectó una posible fuga o presencia "
                "anormal de combustible."
            ),

        "recomendaciones": [
            "Evitar fuentes de ignición cerca del vehículo.",
            "No continuar conduciendo si existe una fuga activa de combustible.",
            "Solicitar una inspección profesional del sistema de combustible."
        ]
    },


    # =====================================================
    # HUMO / GASES EN HABITÁCULO
    # =====================================================

    {
        "codigo":
            "HUMO_HABITACULO",

        "titulo":
            "Humo o gases dentro del habitáculo",

        "patrones": [
            r"\bhumo dentro del auto\b",
            r"\bhumo dentro del vehiculo\b",
            r"\bhumo dentro del habitaculo\b",
            r"\bgases dentro del auto\b",
            r"\bgases dentro del vehiculo\b",
            r"\bgases dentro del habitaculo\b",
            r"\bolor a escape dentro del auto\b"
        ],

        "mensaje":
            (
                "Se detectó la posible presencia de humo "
                "o gases de escape dentro del habitáculo."
            ),

        "recomendaciones": [
            "Evitar permanecer dentro del vehículo si existe presencia real de humo o gases.",
            "Ventilar y detener el vehículo de manera segura.",
            "Solicitar inspección del sistema de escape, ventilación y posibles fugas."
        ]
    },


    # =====================================================
    # RUEDA / NEUMÁTICO
    # =====================================================

    {
        "codigo":
            "RUEDA_CRITICA",

        "titulo":
            "Posible falla crítica de rueda o neumático",

        "patrones": [
            r"\bneumatico reventado\b",
            r"\bneumatico exploto\b",
            r"\bruida suelta\b",
            r"\brueda suelta\b",
            r"\bpernos de rueda sueltos\b"
        ],

        "mensaje":
            (
                "Se detectó una posible condición que puede "
                "comprometer la seguridad de una rueda."
            ),

        "recomendaciones": [
            "No continuar conduciendo con una rueda suelta o un neumático reventado.",
            "Detener el vehículo en un lugar seguro.",
            "Revisar rueda, neumático y fijaciones antes de volver a circular."
        ]
    }
]


# =========================================================
# EVALUAR SEGURIDAD
# =========================================================

def evaluar_seguridad_critica(
    consulta: str
) -> dict:
    """
    Busca señales críticas conocidas utilizando reglas
    deterministas.

    No utiliza inteligencia artificial.
    """

    sintomas = extraer_sintomas(
        consulta
    )


    texto = normalizar_texto(
        sintomas
    )


    alertas_detectadas = []

    recomendaciones = []


    for alerta in ALERTAS_CRITICAS:

        encontrada = False


        for patron in alerta[
            "patrones"
        ]:

            if re.search(
                patron,
                texto
            ):

                encontrada = True

                break


        if encontrada:

            alertas_detectadas.append(
                {
                    "codigo":
                        alerta["codigo"],

                    "titulo":
                        alerta["titulo"],

                    "mensaje":
                        alerta["mensaje"]
                }
            )


            for recomendacion in alerta[
                "recomendaciones"
            ]:

                if recomendacion not in recomendaciones:

                    recomendaciones.append(
                        recomendacion
                    )


    es_critico = (
        len(
            alertas_detectadas
        )
        > 0
    )


    if es_critico:

        advertencia = (
            "AutoDiag AI detectó mediante reglas locales "
            "una o más señales potencialmente críticas. "
            "Por seguridad, estas señales establecen un "
            "nivel mínimo de riesgo alto y requieren "
            "evaluación profesional."
        )

    else:

        advertencia = ""


    return {

        "es_critico":
            es_critico,

        "alertas":
            alertas_detectadas,

        "recomendaciones":
            recomendaciones,

        "advertencia":
            advertencia,

        "nivel_riesgo_minimo":
            (
                "alto"
                if es_critico
                else None
            ),

        "seguridad_conduccion":
            (
                "no_recomendado"
                if es_critico
                else None
            ),

        "requiere_revision_profesional":
            es_critico
    }


# =========================================================
# CONTEXTO PARA LOS AGENTES
# =========================================================

def crear_contexto_seguridad(
    evaluacion: dict
) -> str:
    """
    Genera texto para informar a los agentes de una
    detección crítica local.
    """

    if not evaluacion.get(
        "es_critico"
    ):

        return ""


    alertas = "\n".join(
        f"- {alerta['titulo']}: {alerta['mensaje']}"
        for alerta in evaluacion[
            "alertas"
        ]
    )


    return (
        "\n\n"
        "ALERTA DETERMINISTA DE SEGURIDAD AUTODIAG:\n"
        f"{alertas}\n\n"
        "Regla obligatoria: esta consulta contiene una "
        "señal potencialmente crítica detectada antes "
        "del análisis de IA. El diagnóstico final no "
        "debe reducir el riesgo por debajo de ALTO, "
        "la conducción debe marcarse como NO_RECOMENDADO "
        "y debe requerirse revisión profesional."
    )


# =========================================================
# APLICAR GUARDIA AL RESULTADO
# =========================================================

def aplicar_guardia_seguridad(
    resultado: dict,
    evaluacion: dict
) -> dict:
    """
    Aplica una protección final al diagnóstico.

    Si existe una señal crítica local, el LLM no puede
    reducir el nivel de seguridad establecido.
    """

    resultado_final = deepcopy(
        resultado
    )


    if not evaluacion.get(
        "es_critico"
    ):

        return resultado_final


    # =====================================================
    # CAMPOS OBLIGATORIOS
    # =====================================================

    resultado_final[
        "nivel_riesgo"
    ] = "alto"


    resultado_final[
        "seguridad_conduccion"
    ] = "no_recomendado"


    resultado_final[
        "requiere_revision_profesional"
    ] = True


    # =====================================================
    # EVALUACIÓN DE SEGURIDAD
    # =====================================================

    titulos = ", ".join(
        alerta[
            "titulo"
        ]
        for alerta in evaluacion[
            "alertas"
        ]
    )


    mensaje_seguridad = (
        "Alerta de seguridad local: "
        f"{titulos}. "
        "Por precaución, AutoDiag AI considera "
        "que no es recomendable continuar conduciendo "
        "hasta realizar una evaluación profesional."
    )


    evaluacion_existente = str(
        resultado_final.get(
            "evaluacion_seguridad",
            ""
        )
    ).strip()


    if evaluacion_existente:

        resultado_final[
            "evaluacion_seguridad"
        ] = (
            mensaje_seguridad
            + " "
            + evaluacion_existente
        )

    else:

        resultado_final[
            "evaluacion_seguridad"
        ] = mensaje_seguridad


    # =====================================================
    # RECOMENDACIONES
    # =====================================================

    recomendaciones_actuales = list(
        resultado_final.get(
            "recomendaciones",
            []
        )
    )


    nuevas_recomendaciones = []


    for recomendacion in evaluacion[
        "recomendaciones"
    ]:

        if recomendacion not in nuevas_recomendaciones:

            nuevas_recomendaciones.append(
                recomendacion
            )


    for recomendacion in recomendaciones_actuales:

        if recomendacion not in nuevas_recomendaciones:

            nuevas_recomendaciones.append(
                recomendacion
            )


    # Mantener el informe compacto.
    resultado_final[
        "recomendaciones"
    ] = nuevas_recomendaciones[
        :5
    ]


    # =====================================================
    # ADVERTENCIA
    # =====================================================

    advertencia_existente = str(
        resultado_final.get(
            "advertencia",
            ""
        )
    ).strip()


    advertencia_local = evaluacion[
        "advertencia"
    ]


    if advertencia_existente:

        resultado_final[
            "advertencia"
        ] = (
            advertencia_local
            + " "
            + advertencia_existente
        )

    else:

        resultado_final[
            "advertencia"
        ] = advertencia_local


    return resultado_final