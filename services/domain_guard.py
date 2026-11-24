import re
import unicodedata


# =========================================================
# EXCEPCIÓN
# =========================================================

class ConsultaFueraDeDominioError(ValueError):
    """
    Error utilizado cuando una consulta no pertenece
    claramente al dominio automotriz.
    """

    pass


# =========================================================
# CONFIGURACIÓN
# =========================================================

PUNTAJE_MINIMO = 3


# =========================================================
# FRASES AUTOMOTRICES FUERTES
# =========================================================

FRASES_AUTOMOTRICES = {

    "no arranca",
    "no enciende",
    "se apaga el motor",
    "motor se apaga",

    "pierde potencia",
    "perdida de potencia",

    "ralenti inestable",

    "volante vibra",
    "volante tiembla",
    "volante duro",

    "vibra al frenar",
    "vibracion al frenar",

    "ruido al frenar",
    "ruido al acelerar",
    "ruido al girar",
    "ruido al pasar baches",

    "golpe al pasar baches",

    "pedal de freno",
    "pedal de embrague",

    "suben las revoluciones",
    "suben las rpm",

    "dificultad para pasar cambios",
    "dificultad para meter cambios",

    "motor se calienta",
    "temperatura del motor",
    "pierde refrigerante",

    "bateria se descarga",
    "bateria descargada",
    "luces debiles",

    "check engine",
    "testigo de motor",
    "codigo de falla",

    "humo por el escape",
    "olor a gasolina",
    "olor a bencina",
    "olor a gases",

    "aire acondicionado no enfria",

    "caja automatica",
    "caja manual",
    "caja de cambios",

    "direccion asistida",

    "presion de neumaticos",
    "presion de aceite",

    "sistema de frenos",
    "sistema de carga",
    "sistema de refrigeracion",
    "sistema electrico",

    "diagnostico automotriz",
    "mantenimiento automotriz"
}


# =========================================================
# TÉRMINOS AUTOMOTRICES FUERTES
# =========================================================

TERMINOS_FUERTES = {

    # Vehículo
    "auto",
    "automovil",
    "vehiculo",
    "coche",

    # Motor
    "motor",
    "bujia",
    "bujias",
    "bobina",
    "bobinas",
    "inyector",
    "inyectores",
    "inyeccion",
    "ralenti",

    # Frenos
    "freno",
    "frenos",
    "pastilla",
    "pastillas",

    # Electricidad
    "bateria",
    "alternador",
    "fusible",
    "fusibles",

    # Transmisión
    "embrague",
    "transmision",
    "marchas",
    "rpm",

    # Refrigeración
    "refrigerante",
    "radiador",
    "termostato",

    # Suspensión
    "suspension",
    "amortiguador",
    "amortiguadores",
    "bieleta",
    "bieletas",
    "rotula",
    "rotulas",

    # Dirección
    "direccion",
    "volante",

    # Ruedas
    "neumatico",
    "neumaticos",
    "llanta",
    "llantas",
    "alineacion",
    "balanceo",

    # Motor / admisión
    "turbo",
    "turbocompresor",

    # Escape
    "escape",
    "catalizador",

    # Diagnóstico
    "obd",
    "obd2",
    "ecu",

    # Acciones típicamente automotrices
    "frenar",
    "acelerar",
    "arrancar"
}


# =========================================================
# TÉRMINOS QUE NECESITAN CONTEXTO
# =========================================================

TERMINOS_CONTEXTUALES = {

    "aceite",
    "presion",
    "temperatura",

    "sensor",
    "sensores",

    "filtro",
    "filtros",

    "caja",

    "ruido",
    "ruidos",

    "vibracion",
    "vibra",
    "tiembla",

    "golpe",
    "golpes",

    "humo",

    "olor",

    "potencia",

    "revision",

    "mantenimiento",
    "mantencion",

    "voltaje",

    "combustible",
    "gasolina",
    "bencina",
    "diesel",

    "electrico",
    "electrica",

    "ventilador",

    "compresor",

    "testigo",

    "tablero",

    "revoluciones",

    "kilometraje"
}


# =========================================================
# TÉRMINOS TÉCNICOS AUTOMOTRICES ADICIONALES
# =========================================================

TERMINOS_TECNICOS = {

    "maf",
    "map",
    "lambda",

    "sensor maf",
    "sensor map",
    "sensor de oxigeno",

    "abs",
    "esp",

    "dpf",
    "fap",

    "egr",

    "common rail",

    "adblue",

    "correa distribucion",
    "cadena distribucion",

    "volante motor",

    "homocinetica",
    "homocineticas"
}


# =========================================================
# NORMALIZACIÓN
# =========================================================

def normalizar_texto(
    texto: str
) -> str:
    """
    Convierte texto a minúsculas, elimina tildes
    y caracteres innecesarios.
    """

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
# EXTRAER SÍNTOMA
# =========================================================

def extraer_consulta_relevante(
    consulta: str
) -> str:
    """
    Cuando la consulta contiene información del vehículo
    más una sección de síntomas, analiza únicamente
    los síntomas.

    Esto evita que escribir una marca o modelo haga
    pasar automáticamente una pregunta fuera de dominio.
    """

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


    return str(
        consulta
    ).strip()


# =========================================================
# BUSCAR TÉRMINO
# =========================================================

def contiene_termino(
    texto: str,
    termino: str
) -> bool:

    termino = normalizar_texto(
        termino
    )


    if not termino:

        return False


    if " " in termino:

        return termino in texto


    patron = (
        rf"\b"
        rf"{re.escape(termino)}"
        rf"\b"
    )


    return (
        re.search(
            patron,
            texto
        )
        is not None
    )


# =========================================================
# EVALUAR DOMINIO
# =========================================================

def evaluar_dominio_automotriz(
    consulta: str
) -> dict:
    """
    Evalúa localmente si una consulta pertenece
    razonablemente al dominio automotriz.

    La puntuación es una herramienta interna.
    No representa confianza estadística.
    """

    consulta_relevante = (
        extraer_consulta_relevante(
            consulta
        )
    )


    texto = normalizar_texto(
        consulta_relevante
    )


    if not texto:

        return {

            "es_automotriz":
                False,

            "puntaje":
                0,

            "coincidencias_fuertes":
                [],

            "coincidencias_contextuales":
                [],

            "consulta_relevante":
                ""
        }


    puntaje = 0

    coincidencias_fuertes = []

    coincidencias_contextuales = []


    # =====================================================
    # FRASES FUERTES
    # =====================================================

    for frase in FRASES_AUTOMOTRICES:

        frase_normalizada = (
            normalizar_texto(
                frase
            )
        )


        if frase_normalizada in texto:

            coincidencias_fuertes.append(
                frase
            )

            puntaje += 4


    # =====================================================
    # TÉRMINOS TÉCNICOS
    # =====================================================

    for termino in TERMINOS_TECNICOS:

        if contiene_termino(
            texto,
            termino
        ):

            coincidencias_fuertes.append(
                termino
            )

            puntaje += 4


    # =====================================================
    # TÉRMINOS FUERTES
    # =====================================================

    for termino in TERMINOS_FUERTES:

        if contiene_termino(
            texto,
            termino
        ):

            coincidencias_fuertes.append(
                termino
            )

            puntaje += 3


    # =====================================================
    # CONTEXTUALES
    # =====================================================

    for termino in TERMINOS_CONTEXTUALES:

        if contiene_termino(
            texto,
            termino
        ):

            coincidencias_contextuales.append(
                termino
            )

            puntaje += 1


    coincidencias_fuertes = list(
        dict.fromkeys(
            coincidencias_fuertes
        )
    )


    coincidencias_contextuales = list(
        dict.fromkeys(
            coincidencias_contextuales
        )
    )


    # =====================================================
    # DECISIÓN
    # =====================================================

    tiene_indicio_fuerte = (
        len(
            coincidencias_fuertes
        )
        > 0
    )


    tiene_contexto_suficiente = (
        len(
            coincidencias_contextuales
        )
        >= 3
    )


    es_automotriz = (

        puntaje >= PUNTAJE_MINIMO

        and (

            tiene_indicio_fuerte

            or tiene_contexto_suficiente
        )
    )


    return {

        "es_automotriz":
            es_automotriz,

        "puntaje":
            puntaje,

        "coincidencias_fuertes":
            coincidencias_fuertes,

        "coincidencias_contextuales":
            coincidencias_contextuales,

        "consulta_relevante":
            consulta_relevante
    }


# =========================================================
# VALIDAR
# =========================================================

def validar_consulta_automotriz(
    consulta: str
) -> dict:
    """
    Rechaza consultas que no presenten suficiente
    evidencia de pertenecer al dominio automotriz.
    """

    resultado = (
        evaluar_dominio_automotriz(
            consulta
        )
    )


    if not resultado[
        "es_automotriz"
    ]:

        raise ConsultaFueraDeDominioError(
            "AutoDiag AI está diseñado exclusivamente "
            "para consultas relacionadas con vehículos, "
            "diagnóstico automotriz, fallas mecánicas, "
            "sistemas eléctricos, mantenimiento y "
            "funcionamiento del automóvil."
        )


    return resultado