import re
import unicodedata

from crewai.tools import tool


# =========================================================
# BASE ESTRUCTURADA DE DIAGNÓSTICO
# =========================================================

PROBLEMAS = {

    # =====================================================
    # FRENOS
    # =====================================================

    "frenos": {

        "nombre":
            "Sistema de frenos",

        "sintomas": [
            "vibracion al frenar",
            "volante tiembla al frenar",
            "ruido metalico al frenar",
            "chirrido al frenar",
            "pedal de freno esponjoso",
            "pedal de freno duro",
            "frenado debil",
            "el auto se va hacia un lado al frenar",
            "perdida de liquido de frenos"
        ],

        "palabras_clave": [
            "freno",
            "frenar",
            "pastillas",
            "discos",
            "liquido de frenos",
            "pedal de freno"
        ],

        "causas": [
            "Pastillas de freno desgastadas o deterioradas.",
            "Discos de freno con desgaste irregular o deformación.",
            "Problemas en pinzas u otros componentes del sistema.",
            "Problemas en el circuito hidráulico o líquido de frenos."
        ],

        "riesgo":
            "alto"
    },


    # =====================================================
    # BATERÍA
    # =====================================================

    "bateria": {

        "nombre":
            "Batería",

        "sintomas": [
            "dificultad para arrancar",
            "no arranca",
            "luces debiles",
            "motor de arranque lento",
            "clic al intentar arrancar",
            "bateria descargada",
            "bateria se descarga",
            "bateria se descarga rapido"
        ],

        "palabras_clave": [
            "bateria",
            "arranque lento",
            "luces debiles",
            "descargada",
            "descarga bateria"
        ],

        "causas": [
            "Batería descargada.",
            "Batería deteriorada o con capacidad reducida.",
            "Terminales o conexiones eléctricas deficientes.",
            "Problemas en el sistema de carga."
        ],

        "riesgo":
            "medio"
    },


    # =====================================================
    # SISTEMA ELÉCTRICO / ALTERNADOR
    # =====================================================

    "sistema_electrico": {

        "nombre":
            "Sistema eléctrico y de carga",

        "sintomas": [
            "bateria se descarga aunque es nueva",
            "luces cambian de intensidad",
            "luces parpadean",
            "fallas electricas",
            "problemas electricos",
            "testigo de bateria",
            "bateria no carga",
            "accesorios electricos fallan"
        ],

        "palabras_clave": [
            "alternador",
            "sistema de carga",
            "fallas electricas",
            "testigo bateria",
            "voltaje",
            "electricidad"
        ],

        "causas": [
            "Problemas en el alternador o regulador de carga.",
            "Conexiones eléctricas deficientes.",
            "Cableado o terminales deteriorados.",
            "Consumo eléctrico anormal con el vehículo detenido."
        ],

        "riesgo":
            "medio"
    },


    # =====================================================
    # MOTOR
    # =====================================================

    "motor": {

        "nombre":
            "Motor",

        "sintomas": [
            "tirones",
            "motor tironea",
            "perdida de potencia",
            "falta de potencia",
            "ralenti inestable",
            "motor se apaga",
            "motor vibra",
            "dificultad para arrancar",
            "motor falla al acelerar",
            "respuesta lenta al acelerar"
        ],

        "palabras_clave": [
            "motor",
            "tirones",
            "potencia",
            "ralenti",
            "bujias",
            "inyeccion",
            "encendido"
        ],

        "causas": [
            "Problemas en el sistema de encendido.",
            "Bujías o bobinas deterioradas.",
            "Problemas en el sistema de inyección o combustible.",
            "Problemas de admisión, sensores o gestión electrónica."
        ],

        "riesgo":
            "medio"
    },


    # =====================================================
    # REFRIGERACIÓN
    # =====================================================

    "refrigeracion": {

        "nombre":
            "Sistema de refrigeración",

        "sintomas": [
            "motor se calienta",
            "temperatura alta",
            "sobrecalentamiento",
            "temperatura del motor sube",
            "pierde refrigerante",
            "nivel de refrigerante baja",
            "ventilador no enciende",
            "motor caliente"
        ],

        "palabras_clave": [
            "refrigerante",
            "sobrecalentamiento",
            "temperatura",
            "radiador",
            "termostato",
            "ventilador",
            "bomba de agua"
        ],

        "causas": [
            "Nivel insuficiente o pérdida de refrigerante.",
            "Problemas en el termostato.",
            "Problemas en el ventilador o su sistema de control.",
            "Problemas en radiador, bomba de agua u otros componentes."
        ],

        "riesgo":
            "alto"
    },


    # =====================================================
    # TRANSMISIÓN / EMBRAGUE
    # =====================================================

    "transmision": {

        "nombre":
            "Transmisión y embrague",

        "sintomas": [
            "dificultad para pasar cambios",
            "dificultad para meter cambios",
            "cambios duros",
            "ruido al cambiar marcha",
            "embrague patina",
            "embrague duro",
            "embrague vibra",
            "rpm suben pero no acelera",
            "revoluciones suben pero no acelera",
            "cambios bruscos"
        ],

        "palabras_clave": [
            "embrague",
            "transmision",
            "caja",
            "cambio",
            "marchas",
            "velocidades",
            "patina"
        ],

        "causas": [
            "Desgaste o funcionamiento incorrecto del embrague.",
            "Problemas en el mecanismo de selección de marchas.",
            "Problemas internos o de lubricación de la transmisión.",
            "Problemas electrónicos o hidráulicos en transmisiones automáticas."
        ],

        "riesgo":
            "medio"
    },


    # =====================================================
    # SUSPENSIÓN
    # =====================================================

    "suspension": {

        "nombre":
            "Suspensión",

        "sintomas": [
            "golpe al pasar baches",
            "golpes en suspension",
            "ruido al pasar baches",
            "auto rebota mucho",
            "vehiculo rebota",
            "inestabilidad en curvas",
            "ruido en suspension",
            "golpeteo en rueda"
        ],

        "palabras_clave": [
            "suspension",
            "amortiguador",
            "bujes",
            "bieletas",
            "rotulas",
            "baches",
            "rebota"
        ],

        "causas": [
            "Amortiguadores deteriorados.",
            "Bujes o bieletas desgastados.",
            "Rótulas u otros elementos con holgura.",
            "Problemas en resortes o fijaciones."
        ],

        "riesgo":
            "medio"
    },


    # =====================================================
    # DIRECCIÓN
    # =====================================================

    "direccion": {

        "nombre":
            "Sistema de dirección",

        "sintomas": [
            "volante duro",
            "direccion dura",
            "ruido al girar volante",
            "holgura en volante",
            "volante tiene juego",
            "direccion imprecisa",
            "volante no vuelve",
            "dificultad para girar"
        ],

        "palabras_clave": [
            "direccion",
            "volante",
            "girar",
            "holgura",
            "direccion asistida"
        ],

        "causas": [
            "Problemas en componentes de la dirección.",
            "Holguras en elementos mecánicos.",
            "Problemas en el sistema de asistencia de dirección.",
            "Problemas relacionados con suspensión, ruedas o alineación."
        ],

        "riesgo":
            "alto"
    },


    # =====================================================
    # NEUMÁTICOS / RUEDAS
    # =====================================================

    "neumaticos": {

        "nombre":
            "Neumáticos y ruedas",

        "sintomas": [
            "volante vibra a velocidad",
            "vibracion a alta velocidad",
            "vibracion a cierta velocidad",
            "desgaste irregular de neumaticos",
            "auto tira hacia un lado",
            "vehiculo se va hacia un lado",
            "neumatico pierde presion",
            "rueda vibra"
        ],

        "palabras_clave": [
            "neumatico",
            "neumaticos",
            "rueda",
            "llanta",
            "alineacion",
            "balanceo",
            "presion"
        ],

        "causas": [
            "Desbalanceo de ruedas.",
            "Problemas de alineación.",
            "Desgaste irregular o daño en neumáticos.",
            "Daños o deformaciones en ruedas o llantas."
        ],

        "riesgo":
            "medio"
    },


    # =====================================================
    # ESCAPE / EMISIONES
    # =====================================================

    "escape": {

        "nombre":
            "Escape y emisiones",

        "sintomas": [
            "humo negro",
            "humo blanco",
            "humo azul",
            "olor a gases",
            "olor a escape",
            "ruido fuerte de escape",
            "gases dentro del auto",
            "humo por escape"
        ],

        "palabras_clave": [
            "escape",
            "humo",
            "gases",
            "catalizador",
            "emisiones",
            "silenciador"
        ],

        "causas": [
            "Problemas en el sistema de escape.",
            "Problemas relacionados con combustión o emisiones.",
            "Fugas en tuberías o uniones del escape.",
            "Problemas en catalizador o sensores relacionados."
        ],

        "riesgo":
            "medio"
    },


    # =====================================================
    # TURBO
    # =====================================================

    "turbo": {

        "nombre":
            "Sistema de sobrealimentación",

        "sintomas": [
            "turbo no carga",
            "perdida de potencia turbo",
            "silbido del turbo",
            "silbido al acelerar",
            "falta de presion turbo",
            "humo y perdida de potencia"
        ],

        "palabras_clave": [
            "turbo",
            "turbocompresor",
            "sobrealimentacion",
            "presion turbo"
        ],

        "causas": [
            "Problemas en conductos de admisión o presión.",
            "Problemas de control de sobrealimentación.",
            "Problemas en sensores asociados.",
            "Posible deterioro del turbocompresor."
        ],

        "riesgo":
            "medio"
    },


    # =====================================================
    # ELECTRÓNICA / SENSORES
    # =====================================================

    "electronica": {

        "nombre":
            "Electrónica y sensores",

        "sintomas": [
            "check engine",
            "testigo motor",
            "luz de motor encendida",
            "testigos en tablero",
            "error en tablero",
            "falla sensor",
            "fallas intermitentes",
            "modo emergencia"
        ],

        "palabras_clave": [
            "sensor",
            "sensores",
            "check engine",
            "testigo",
            "codigo de falla",
            "diagnostico electronico",
            "ecu"
        ],

        "causas": [
            "Algún sistema electrónico detectó una anomalía.",
            "Problemas en sensores o sus conexiones.",
            "Problemas de alimentación eléctrica o cableado.",
            "Una falla en otro sistema puede haber generado el código."
        ],

        "riesgo":
            "medio"
    },


    # =====================================================
    # CLIMATIZACIÓN
    # =====================================================

    "climatizacion": {

        "nombre":
            "Climatización y aire acondicionado",

        "sintomas": [
            "aire acondicionado no enfria",
            "aire sale caliente",
            "aire acondicionado enfria poco",
            "ventilador interior no funciona",
            "ruido al prender aire acondicionado",
            "compresor hace ruido"
        ],

        "palabras_clave": [
            "aire acondicionado",
            "climatizacion",
            "compresor",
            "refrigerante aire",
            "ventilador interior"
        ],

        "causas": [
            "Nivel insuficiente de refrigerante del sistema.",
            "Posible fuga en el circuito.",
            "Problemas en el compresor.",
            "Problemas eléctricos, sensores o ventiladores."
        ],

        "riesgo":
            "bajo"
    }
}


# =========================================================
# NORMALIZACIÓN
# =========================================================

def normalizar_texto(
    texto: str
) -> str:
    """
    Convierte el texto a una representación uniforme
    para facilitar las coincidencias.
    """

    texto = (
        texto
        .lower()
        .strip()
    )


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
# PUNTUACIÓN DE COINCIDENCIA
# =========================================================

def calcular_puntaje(
    texto: str,
    datos: dict
) -> int:
    """
    Calcula qué tan relacionado está un texto
    con un sistema determinado.

    El valor se utiliza únicamente de forma interna.
    No representa un porcentaje de certeza.
    """

    puntaje = 0


    # =====================================================
    # SÍNTOMAS CONOCIDOS
    # =====================================================

    for sintoma in datos[
        "sintomas"
    ]:

        sintoma_normalizado = (
            normalizar_texto(
                sintoma
            )
        )


        if (
            sintoma_normalizado
            in texto
        ):

            # Las frases completas tienen mayor peso.
            puntaje += 5


    # =====================================================
    # PALABRAS CLAVE
    # =====================================================

    for palabra in datos[
        "palabras_clave"
    ]:

        palabra_normalizada = (
            normalizar_texto(
                palabra
            )
        )


        if (
            palabra_normalizada
            in texto
        ):

            puntaje += 1


    return puntaje


# =========================================================
# BUSCAR SISTEMAS RELACIONADOS
# =========================================================

def encontrar_sistemas(
    sintoma: str,
    limite: int = 3
) -> list[dict]:
    """
    Busca los sistemas automotrices más relacionados
    con los síntomas escritos por el usuario.
    """

    texto = normalizar_texto(
        sintoma
    )


    resultados = []


    for categoria, datos in PROBLEMAS.items():

        puntaje = calcular_puntaje(
            texto,
            datos
        )


        if puntaje > 0:

            resultados.append(
                {
                    "categoria":
                        categoria,

                    "nombre":
                        datos[
                            "nombre"
                        ],

                    "puntaje":
                        puntaje,

                    "causas":
                        datos[
                            "causas"
                        ],

                    "riesgo":
                        datos[
                            "riesgo"
                        ]
                }
            )


    resultados.sort(
        key=lambda resultado:
            resultado["puntaje"],
        reverse=True
    )


    return resultados[
        :limite
    ]


# =========================================================
# DIAGNÓSTICO BASE
# =========================================================

def diagnosticar_sintoma_base(
    sintoma: str
) -> str:
    """
    Analiza los síntomas utilizando la base
    estructurada de AutoDiag AI.
    """

    resultados = encontrar_sistemas(
        sintoma=sintoma,
        limite=3
    )


    # =====================================================
    # SIN COINCIDENCIAS
    # =====================================================

    if not resultados:

        return (
            "No se encontró una coincidencia directa "
            "en la base estructurada de síntomas.\n\n"
            "El síntoma debe evaluarse utilizando "
            "el conocimiento técnico RAG y el análisis "
            "del especialista mecánico.\n\n"
            "No debe asumirse una causa sin evidencia."
        )


    principal = resultados[0]


    causas_texto = "\n".join(
        f"- {causa}"
        for causa
        in principal[
            "causas"
        ]
    )


    respuesta = (
        f"Sistema principal relacionado: "
        f"{principal['nombre']}\n\n"
        f"Categoría interna: "
        f"{principal['categoria']}\n\n"
        f"Nivel general de riesgo: "
        f"{principal['riesgo']}\n\n"
        f"Posibles causas:\n"
        f"{causas_texto}"
    )


    # =====================================================
    # SISTEMAS ALTERNATIVOS
    # =====================================================

    if len(resultados) > 1:

        alternativos = []


        for resultado in resultados[
            1:
        ]:

            alternativos.append(
                f"- {resultado['nombre']}"
            )


        respuesta += (
            "\n\nOtros sistemas que podrían "
            "estar relacionados:\n"
            + "\n".join(
                alternativos
            )
        )


    respuesta += (
        "\n\nLas causas indicadas son hipótesis "
        "orientativas y no representan un "
        "diagnóstico confirmado."
    )


    return respuesta


# =========================================================
# HERRAMIENTA CREWAI
# =========================================================

@tool("Diagnosticar síntoma automotriz")
def diagnosticar_sintoma(
    sintoma: str
) -> str:
    """
    Analiza síntomas automotrices utilizando la base
    estructurada de AutoDiag AI.

    Utiliza esta herramienta cuando el usuario describa
    fallas, ruidos, vibraciones, pérdida de potencia,
    problemas eléctricos o cualquier comportamiento
    anormal del vehículo.

    La herramienta devuelve sistemas relacionados,
    posibles causas y nivel general de riesgo.

    La información obtenida es orientativa y no
    representa un diagnóstico definitivo.
    """

    return diagnosticar_sintoma_base(
        sintoma
    )