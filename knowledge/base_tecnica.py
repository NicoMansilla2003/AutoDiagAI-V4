from langchain_core.documents import Document


# =========================================================
# VERSIÓN DE LA BASE DE CONOCIMIENTO
# =========================================================

BASE_CONOCIMIENTO_VERSION = "2.0.0"


# =========================================================
# DOCUMENTOS TÉCNICOS
# =========================================================

DOCUMENTOS = [

    # =====================================================
    # FRENOS
    # =====================================================

    Document(
        page_content="""
        Sistema de frenos:

        Una vibración durante el frenado puede estar relacionada
        con desgaste irregular de componentes, deformación de discos
        o problemas en otros elementos del sistema de frenos.

        Entre los componentes que pueden inspeccionarse se encuentran
        las pastillas, discos, pinzas, líquido de frenos y elementos
        relacionados con el montaje de las ruedas.

        Si la vibración aparece principalmente al presionar el pedal
        de freno, el sistema de frenos debe considerarse una de las
        primeras áreas de inspección.

        Si existen síntomas que puedan comprometer la capacidad de
        frenado, el vehículo debe ser evaluado por un profesional
        antes de continuar utilizándolo normalmente.
        """,

        metadata={
            "categoria": "frenos",
            "subcategoria": "vibraciones",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    Document(
        page_content="""
        Ruidos en los frenos:

        Los ruidos metálicos, chirridos o roces durante el frenado
        pueden estar relacionados con desgaste de las pastillas,
        presencia de suciedad, contacto irregular entre componentes
        o deterioro de discos y elementos de fijación.

        Un ruido metálico persistente puede indicar que un componente
        de fricción se encuentra excesivamente desgastado.

        Si el ruido está acompañado de pérdida de capacidad de frenado,
        vibraciones fuertes o comportamiento anormal del pedal,
        se recomienda detener el uso normal del vehículo y realizar
        una inspección profesional.
        """,

        metadata={
            "categoria": "frenos",
            "subcategoria": "ruidos",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    Document(
        page_content="""
        Pedal de freno:

        Un pedal excesivamente esponjoso puede estar relacionado con
        presencia de aire en el circuito hidráulico, pérdida de líquido
        o problemas en componentes del sistema.

        Un pedal anormalmente duro puede relacionarse con problemas
        en la asistencia de frenado u otros elementos mecánicos.

        Una modificación repentina en la sensación del pedal debe
        considerarse un síntoma importante debido a que puede afectar
        directamente la capacidad de detener el vehículo.
        """,

        metadata={
            "categoria": "frenos",
            "subcategoria": "pedal",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # MOTOR
    # =====================================================

    Document(
        page_content="""
        Motor - tirones y pérdida de potencia:

        Los tirones, falta de respuesta o pérdida de potencia pueden
        estar relacionados con diferentes sistemas del motor.

        Entre las áreas que pueden revisarse se encuentran las bujías,
        bobinas de encendido, alimentación de combustible, inyección,
        admisión de aire y diferentes sensores de gestión electrónica.

        Un mismo síntoma puede tener varias causas, por lo que una
        lectura de códigos de diagnóstico puede ser útil cuando
        la falla persiste.

        AutoDiag AI debe tratar estas causas como hipótesis y no como
        un diagnóstico confirmado.
        """,

        metadata={
            "categoria": "motor",
            "subcategoria": "perdida_potencia",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    Document(
        page_content="""
        Motor - ralentí inestable:

        Un ralentí irregular puede estar relacionado con problemas
        de encendido, admisión de aire, alimentación de combustible,
        inyección, sensores o acumulación de suciedad en algunos
        componentes de admisión.

        También pueden existir diferencias entre un comportamiento
        normal durante el arranque en frío y una falla persistente
        cuando el motor ya se encuentra funcionando normalmente.

        Si el ralentí inestable está acompañado de pérdida importante
        de potencia, testigos de avería o apagado del motor,
        se recomienda realizar diagnóstico electrónico.
        """,

        metadata={
            "categoria": "motor",
            "subcategoria": "ralenti",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    Document(
        page_content="""
        Motor - dificultad para arrancar:

        Una dificultad de arranque puede estar relacionada con batería,
        sistema de arranque, encendido, alimentación de combustible,
        sensores o gestión electrónica del motor.

        Antes de asumir una falla mecánica interna, conviene comprobar
        elementos básicos como estado de batería, conexiones eléctricas
        y comportamiento del motor de arranque.

        Si el motor gira normalmente pero no consigue arrancar,
        pueden requerirse comprobaciones adicionales de combustible,
        encendido y diagnóstico electrónico.
        """,

        metadata={
            "categoria": "motor",
            "subcategoria": "arranque",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # BATERÍA
    # =====================================================

    Document(
        page_content="""
        Batería:

        Una batería descargada o deteriorada puede producir dificultad
        para arrancar, funcionamiento lento del motor de arranque,
        luces débiles y diferentes anomalías eléctricas.

        Se recomienda comprobar el estado de la batería, terminales,
        conexiones y sistema de carga.

        Una batería descargada no necesariamente significa que esté
        defectuosa. También puede existir consumo eléctrico anormal
        con el vehículo detenido o problemas en el sistema de carga.
        """,

        metadata={
            "categoria": "bateria",
            "subcategoria": "estado_bateria",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # ALTERNADOR / CARGA
    # =====================================================

    Document(
        page_content="""
        Sistema de carga y alternador:

        El alternador permite mantener la batería cargada mientras
        el motor está funcionando y suministra energía a diferentes
        sistemas eléctricos del vehículo.

        Síntomas como batería que vuelve a descargarse, luces que
        cambian de intensidad, advertencias eléctricas o problemas
        recurrentes de arranque pueden justificar una revisión
        del sistema de carga.

        Una falla aparente de batería puede originarse realmente
        en un problema del alternador, regulador, cableado o conexiones.
        """,

        metadata={
            "categoria": "sistema_electrico",
            "subcategoria": "alternador",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # EMBRAGUE
    # =====================================================

    Document(
        page_content="""
        Embrague:

        En vehículos con transmisión manual, un embrague desgastado
        puede presentar síntomas como dificultad para transmitir
        correctamente la potencia del motor, aumento de revoluciones
        sin una aceleración proporcional o cambios en el punto
        de acoplamiento del pedal.

        Dificultades para seleccionar marchas también pueden tener
        relación con el sistema de embrague, mecanismos de selección
        o la propia transmisión.

        Un olor intenso después de exigir el embrague puede estar
        relacionado con temperatura elevada por fricción.

        El diagnóstico definitivo requiere inspeccionar el sistema.
        """,

        metadata={
            "categoria": "transmision",
            "subcategoria": "embrague",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # TRANSMISIÓN
    # =====================================================

    Document(
        page_content="""
        Transmisión:

        Problemas para seleccionar marchas, ruidos durante los cambios,
        tirones o comportamientos anormales de la transmisión pueden
        estar relacionados con diferentes componentes mecánicos,
        hidráulicos, electrónicos o de control.

        En transmisiones manuales también debe considerarse el
        funcionamiento del embrague y del mecanismo de selección.

        En transmisiones automáticas, un diagnóstico electrónico puede
        aportar información importante cuando existen testigos,
        cambios bruscos o funcionamiento en modo de emergencia.
        """,

        metadata={
            "categoria": "transmision",
            "subcategoria": "caja_cambios",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # REFRIGERACIÓN
    # =====================================================

    Document(
        page_content="""
        Sistema de refrigeración:

        El sistema de refrigeración mantiene la temperatura del motor
        dentro de un rango adecuado de funcionamiento.

        Un aumento anormal de temperatura puede estar relacionado
        con bajo nivel de refrigerante, pérdidas, problemas del
        termostato, ventilador, bomba de agua, radiador u otros
        componentes del circuito.

        Continuar conduciendo con un motor sobrecalentado puede
        provocar daños importantes.

        Si el indicador muestra temperatura excesiva o aparece una
        advertencia de sobrecalentamiento, se recomienda detener
        el vehículo de manera segura y revisar la situación.
        """,

        metadata={
            "categoria": "refrigeracion",
            "subcategoria": "sobrecalentamiento",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # SUSPENSIÓN
    # =====================================================

    Document(
        page_content="""
        Suspensión:

        Golpes, ruidos al pasar irregularidades, rebotes excesivos
        o sensación de inestabilidad pueden estar relacionados con
        diferentes elementos de la suspensión.

        Entre los componentes que pueden requerir inspección se
        encuentran amortiguadores, resortes, bujes, rótulas,
        bieletas y elementos de fijación.

        Los síntomas de suspensión pueden confundirse con problemas
        de neumáticos, ruedas o dirección, por lo que debe evaluarse
        el conjunto del tren rodante.
        """,

        metadata={
            "categoria": "suspension",
            "subcategoria": "ruidos_inestabilidad",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # DIRECCIÓN
    # =====================================================

    Document(
        page_content="""
        Sistema de dirección:

        Una dirección que se siente más pesada de lo habitual,
        presenta ruidos, holguras o cambios en su comportamiento
        puede estar relacionada con diferentes componentes del
        sistema de dirección.

        También deben considerarse neumáticos, alineación,
        suspensión y estado de elementos mecánicos asociados.

        Si existe pérdida significativa de control, movimientos
        inesperados del volante o dificultad importante para dirigir
        el vehículo, se recomienda evitar continuar la conducción
        hasta realizar una inspección.
        """,

        metadata={
            "categoria": "direccion",
            "subcategoria": "comportamiento",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # NEUMÁTICOS
    # =====================================================

    Document(
        page_content="""
        Neumáticos:

        El estado y presión de los neumáticos tienen influencia directa
        en estabilidad, frenado, consumo y comportamiento del vehículo.

        Vibraciones a determinadas velocidades pueden estar asociadas
        con balanceo de ruedas, deformaciones, desgaste irregular
        o daños en neumáticos y llantas.

        Un vehículo que tiende a desplazarse hacia un lado también
        puede justificar la revisión de presión, neumáticos,
        alineación y componentes de suspensión o dirección.

        Las presiones correctas deben consultarse en la información
        proporcionada por el fabricante del vehículo.
        """,

        metadata={
            "categoria": "neumaticos",
            "subcategoria": "vibraciones_alineacion",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # TURBO
    # =====================================================

    Document(
        page_content="""
        Turbocompresor:

        En motores equipados con turbo, una pérdida de potencia,
        silbidos anormales, determinadas emisiones de humo o
        comportamiento irregular pueden justificar una revisión
        del sistema de sobrealimentación.

        No todos estos síntomas significan necesariamente una falla
        del turbocompresor. También pueden existir problemas en
        conductos de admisión, sensores, control de presión,
        alimentación de combustible u otros componentes.

        Una inspección adecuada debe considerar el conjunto completo
        del sistema antes de sustituir componentes.
        """,

        metadata={
            "categoria": "motor",
            "subcategoria": "turbo",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # ESCAPE
    # =====================================================

    Document(
        page_content="""
        Sistema de escape y emisiones:

        Ruidos anormales debajo del vehículo, olor a gases,
        pérdida de rendimiento o determinados testigos pueden
        justificar una revisión del sistema de escape y emisiones.

        Entre los elementos relacionados pueden encontrarse tuberías,
        uniones, silenciadores, catalizador, sensores y sistemas
        de control de emisiones.

        La presencia de gases de escape dentro del habitáculo
        representa una situación que debe revisarse con rapidez.
        """,

        metadata={
            "categoria": "escape",
            "subcategoria": "emisiones",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # ELECTRÓNICA / SENSORES
    # =====================================================

    Document(
        page_content="""
        Sensores y gestión electrónica:

        Los vehículos modernos utilizan múltiples sensores y módulos
        electrónicos para gestionar motor, seguridad y otros sistemas.

        Un testigo de avería no identifica por sí solo una pieza
        defectuosa. Los códigos de diagnóstico sirven como punto
        de partida para investigar un sistema o condición determinada.

        Sustituir componentes únicamente basándose en un código
        de falla puede llevar a diagnósticos incorrectos.

        La lectura de códigos debe complementarse con síntomas,
        mediciones y otras verificaciones.
        """,

        metadata={
            "categoria": "electronica",
            "subcategoria": "sensores_diagnostico",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # AIRE ACONDICIONADO
    # =====================================================

    Document(
        page_content="""
        Aire acondicionado:

        Si el sistema de climatización deja de enfriar correctamente,
        pueden existir diferentes causas relacionadas con carga
        de refrigerante, compresor, sensores, ventiladores,
        circuito eléctrico o componentes de distribución de aire.

        Una disminución progresiva de rendimiento puede requerir
        comprobar posibles pérdidas antes de realizar únicamente
        una recarga.

        Los trabajos sobre circuitos de refrigerante deben realizarse
        con equipos y procedimientos adecuados.
        """,

        metadata={
            "categoria": "climatizacion",
            "subcategoria": "aire_acondicionado",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # RUIDOS Y VIBRACIONES
    # =====================================================

    Document(
        page_content="""
        Ruidos y vibraciones:

        Los ruidos y vibraciones pueden originarse en múltiples
        sistemas del vehículo.

        Es importante identificar cuándo aparecen: al frenar,
        acelerar, girar, pasar irregularidades, estar detenido
        o circular a una velocidad determinada.

        La velocidad del vehículo, revoluciones del motor,
        posición del volante y uso del freno pueden ayudar
        a diferenciar el origen del síntoma.

        Una descripción detallada mejora significativamente
        la orientación inicial del diagnóstico.
        """,

        metadata={
            "categoria": "diagnostico_general",
            "subcategoria": "ruidos_vibraciones",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # TESTIGOS
    # =====================================================

    Document(
        page_content="""
        Testigos del tablero:

        Los indicadores del tablero permiten advertir sobre diferentes
        condiciones del vehículo.

        El significado exacto de cada símbolo depende del fabricante
        y modelo, por lo que debe consultarse el manual correspondiente.

        Los testigos asociados a presión de aceite, temperatura,
        sistema de frenos u otras condiciones críticas requieren
        especial atención.

        Un testigo de diagnóstico del motor normalmente indica que
        el sistema electrónico ha detectado una condición que debe
        investigarse mediante diagnóstico apropiado.
        """,

        metadata={
            "categoria": "diagnostico_general",
            "subcategoria": "testigos",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    ),


    # =====================================================
    # MANTENIMIENTO
    # =====================================================

    Document(
        page_content="""
        Mantenimiento preventivo:

        El mantenimiento preventivo permite detectar problemas antes
        de que se conviertan en fallas mayores.

        Entre las áreas generales de revisión pueden encontrarse
        lubricación, frenos, neumáticos, batería, refrigeración,
        filtros, iluminación y diferentes fluidos.

        Los intervalos exactos deben determinarse utilizando
        el programa de mantenimiento definido por el fabricante
        para cada vehículo, motorización y condición de uso.

        AutoDiag AI no debe inventar intervalos de mantenimiento
        específicos cuando no dispone de documentación oficial.
        """,

        metadata={
            "categoria": "mantenimiento",
            "subcategoria": "preventivo",
            "fuente": "base_tecnica_autodiag",
            "version": BASE_CONOCIMIENTO_VERSION
        }
    )
]