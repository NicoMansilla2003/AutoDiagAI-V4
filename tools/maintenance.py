from crewai.tools import tool


# =========================================================
# BASE DE MANTENIMIENTO
# =========================================================

MANTENIMIENTO = {

    # =====================================================
    # FRENOS
    # =====================================================

    "frenos": [

        "Revisar periódicamente el estado de las pastillas de freno.",

        "Inspeccionar discos por desgaste, deformaciones o daños.",

        "Comprobar el nivel y estado del líquido de frenos.",

        "Revisar posibles fugas y el estado general "
        "del sistema hidráulico."
    ],


    # =====================================================
    # BATERÍA
    # =====================================================

    "bateria": [

        "Comprobar periódicamente el estado y voltaje de la batería.",

        "Revisar que los terminales estén limpios y correctamente ajustados.",

        "Observar si existen dificultades recurrentes de arranque.",

        "Comprobar el sistema de carga cuando la batería "
        "se descarga repetidamente."
    ],


    # =====================================================
    # SISTEMA ELÉCTRICO
    # =====================================================

    "sistema_electrico": [

        "Revisar terminales y conexiones eléctricas principales.",

        "Comprobar el funcionamiento del alternador y sistema de carga.",

        "Inspeccionar cableado visible cuando existan fallas eléctricas.",

        "Evitar mantener accesorios eléctricos conectados "
        "innecesariamente con el motor apagado."
    ],


    # =====================================================
    # MOTOR
    # =====================================================

    "motor": [

        "Realizar cambios de aceite y filtros según "
        "el programa indicado por el fabricante.",

        "Revisar periódicamente bujías y componentes "
        "del sistema de encendido cuando corresponda.",

        "Observar cambios en ralentí, potencia, consumo "
        "o comportamiento del motor.",

        "Realizar diagnóstico electrónico cuando aparezcan "
        "fallas persistentes o testigos."
    ],


    # =====================================================
    # REFRIGERACIÓN
    # =====================================================

    "refrigeracion": [

        "Comprobar el nivel de refrigerante con el motor frío.",

        "Inspeccionar visualmente posibles fugas.",

        "Revisar periódicamente mangueras y componentes visibles.",

        "Consultar el programa del fabricante para el reemplazo "
        "del refrigerante."
    ],


    # =====================================================
    # TRANSMISIÓN
    # =====================================================

    "transmision": [

        "Observar cualquier cambio en la suavidad al seleccionar marchas.",

        "Evitar mantener innecesariamente el embrague parcialmente accionado.",

        "Revisar posibles pérdidas de fluido de transmisión cuando corresponda.",

        "Consultar los intervalos de mantenimiento específicos "
        "de la transmisión indicados por el fabricante."
    ],


    # =====================================================
    # SUSPENSIÓN
    # =====================================================

    "suspension": [

        "Inspeccionar amortiguadores si aparecen rebotes excesivos.",

        "Revisar bujes, bieletas y rótulas ante ruidos o golpes.",

        "Observar desgaste irregular de los neumáticos.",

        "Realizar una inspección del tren rodante "
        "si cambia la estabilidad del vehículo."
    ],


    # =====================================================
    # DIRECCIÓN
    # =====================================================

    "direccion": [

        "Revisar cualquier cambio importante en el esfuerzo del volante.",

        "Inspeccionar posibles holguras o ruidos del sistema.",

        "Mantener correctamente la alineación de las ruedas.",

        "Realizar una inspección profesional ante cambios "
        "repentinos en el comportamiento de la dirección."
    ],


    # =====================================================
    # NEUMÁTICOS
    # =====================================================

    "neumaticos": [

        "Comprobar regularmente la presión recomendada por el fabricante.",

        "Inspeccionar desgaste, cortes, deformaciones y daños visibles.",

        "Revisar alineación si existe desgaste irregular "
        "o tendencia a desviarse hacia un lado.",

        "Realizar balanceo cuando aparezcan vibraciones "
        "relacionadas con la velocidad."
    ],


    # =====================================================
    # ESCAPE
    # =====================================================

    "escape": [

        "Inspeccionar el sistema ante ruidos anormales o vibraciones.",

        "Revisar posibles fugas cuando exista olor a gases.",

        "Observar cambios anormales en las emisiones visibles.",

        "Realizar diagnóstico si aparecen testigos "
        "relacionados con emisiones."
    ],


    # =====================================================
    # TURBO
    # =====================================================

    "turbo": [

        "Mantener correctamente los intervalos de cambio de aceite.",

        "Utilizar lubricante con la especificación indicada "
        "por el fabricante.",

        "Revisar conductos de admisión ante pérdidas de potencia.",

        "Consultar a un profesional ante silbidos nuevos, "
        "humo anormal o pérdida significativa de rendimiento."
    ],


    # =====================================================
    # ELECTRÓNICA
    # =====================================================

    "electronica": [

        "No sustituir componentes únicamente por la presencia "
        "de un código de falla.",

        "Realizar lectura de códigos cuando aparezcan "
        "testigos persistentes.",

        "Revisar batería y sistema de carga antes de atribuir "
        "múltiples errores a módulos electrónicos.",

        "Inspeccionar conectores y cableado cuando existan "
        "fallas intermitentes."
    ],


    # =====================================================
    # CLIMATIZACIÓN
    # =====================================================

    "climatizacion": [

        "Utilizar periódicamente el sistema de climatización.",

        "Revisar el filtro de habitáculo según "
        "el programa del fabricante.",

        "Inspeccionar el sistema si existe una disminución "
        "progresiva de la capacidad de enfriamiento.",

        "Evitar realizar recargas de refrigerante repetidas "
        "sin comprobar posibles fugas."
    ]
}


# =========================================================
# NOMBRES VISIBLES
# =========================================================

NOMBRES_CATEGORIAS = {

    "frenos":
        "Sistema de frenos",

    "bateria":
        "Batería",

    "sistema_electrico":
        "Sistema eléctrico y de carga",

    "motor":
        "Motor",

    "refrigeracion":
        "Sistema de refrigeración",

    "transmision":
        "Transmisión y embrague",

    "suspension":
        "Suspensión",

    "direccion":
        "Sistema de dirección",

    "neumaticos":
        "Neumáticos y ruedas",

    "escape":
        "Escape y emisiones",

    "turbo":
        "Turbocompresor",

    "electronica":
        "Electrónica y sensores",

    "climatizacion":
        "Climatización y aire acondicionado"
}


# =========================================================
# OBTENER CATEGORÍAS
# =========================================================

def obtener_categorias_mantenimiento() -> list[str]:

    return list(
        MANTENIMIENTO.keys()
    )


# =========================================================
# NOMBRE VISIBLE
# =========================================================

def obtener_nombre_categoria(
    categoria: str
) -> str:

    return NOMBRES_CATEGORIAS.get(
        categoria,
        categoria.capitalize()
    )


# =========================================================
# INFORMACIÓN ESTRUCTURADA
# =========================================================

def obtener_mantenimiento(
    categoria: str
) -> dict:

    categoria_normalizada = (
        categoria
        .lower()
        .strip()
    )


    recomendaciones = (
        MANTENIMIENTO.get(
            categoria_normalizada
        )
    )


    if not recomendaciones:

        return {

            "categoria":
                categoria_normalizada,

            "nombre":
                "Categoría desconocida",

            "recomendaciones":
                []
        }


    return {

        "categoria":
            categoria_normalizada,

        "nombre":
            obtener_nombre_categoria(
                categoria_normalizada
            ),

        "recomendaciones":
            recomendaciones
    }


# =========================================================
# TEXTO PARA CREWAI
# =========================================================

def consultar_mantenimiento_base(
    categoria: str
) -> str:

    datos = obtener_mantenimiento(
        categoria
    )


    if not datos[
        "recomendaciones"
    ]:

        return (
            f"No se encontró información "
            f"de mantenimiento para "
            f"la categoría '{categoria}'."
        )


    texto_recomendaciones = "\n".join(

        f"- {recomendacion}"

        for recomendacion
        in datos[
            "recomendaciones"
        ]
    )


    return (
        f"Categoría: {datos['nombre']}\n"
        f"Recomendaciones de mantenimiento:\n"
        f"{texto_recomendaciones}"
    )


# =========================================================
# HERRAMIENTA CREWAI
# =========================================================

@tool("Consultar mantenimiento automotriz")
def consultar_mantenimiento(
    categoria: str
) -> str:
    """
    Consulta recomendaciones de mantenimiento preventivo
    para diferentes sistemas del vehículo.

    Utiliza esta herramienta cuando necesites información
    básica de mantenimiento relacionada con frenos, motor,
    batería, transmisión, suspensión, dirección, neumáticos,
    refrigeración, electrónica u otros sistemas registrados.

    Los intervalos específicos deben obtenerse siempre
    desde documentación oficial del fabricante.
    """

    return consultar_mantenimiento_base(
        categoria
    )