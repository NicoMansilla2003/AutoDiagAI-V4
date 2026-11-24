from html import escape
from textwrap import dedent

import streamlit as st

from crew import (
    ejecutar_diagnostico
)

from rag.vectorstore import (
    buscar_documentos_vectoriales,
    obtener_info_base
)

from services.domain_guard import (
    ConsultaFueraDeDominioError,
    validar_consulta_automotriz
)

from services.safety_guard import (
    evaluar_seguridad_critica
)

from services.email_service import (
    enviar_informe_gmail,
    obtener_correo_destino
)

from services.history import (
    inicializar_db,
    guardar_diagnostico,
    listar_diagnosticos,
    obtener_diagnostico
)

from services.auth_service import (
    initialize_auth_db,
    resolve_session,
)

from tools.maintenance import (
    obtener_categorias_mantenimiento,
    obtener_nombre_categoria,
    obtener_mantenimiento
)

from ui.styles import (
    cargar_estilos
)

from ui.auth_views import (
    mostrar_acceso,
    mostrar_usuario_sidebar,
)


# =========================================================
# CONFIGURACIÓN STREAMLIT
# =========================================================

st.set_page_config(
    page_title="AutoDiag AI V4",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)


cargar_estilos()

inicializar_db()
initialize_auth_db()

usuario_actual = resolve_session(
    st.session_state.get("auth_token")
)

if usuario_actual is None:
    st.session_state.pop("auth_token", None)
    mostrar_acceso()
    st.stop()


# =========================================================
# HTML
# =========================================================

def html(
    contenido: str
):

    st.html(
        dedent(
            contenido
        ).strip()
    )


# =========================================================
# ESTADO DE SESIÓN
# =========================================================

def inicializar_estado():

    valores = {

        "resultado_diagnostico":
            None,

        "diagnostico_ejecutado":
            False,

        "ultimo_vehiculo":
            {},

        "ultimo_sintoma":
            "",

        "diagnostico_guardado_id":
            None,

        "historial_abierto_id":
            None,

        "confirmar_email":
            False,

        "resultados_conocimiento":
            [],

        "consulta_conocimiento":
            ""
    }


    for clave, valor in valores.items():

        if clave not in st.session_state:

            st.session_state[
                clave
            ] = valor


inicializar_estado()


# =========================================================
# AGENTES
# =========================================================

def tarjeta_agente(
    icono,
    nombre,
    descripcion,
    estado="ready"
):

    clase = ""

    texto_estado = "LISTO"

    clase_estado = ""


    if estado == "running":

        clase = "running"

        texto_estado = "● ANALIZANDO"

        clase_estado = (
            "agent-status-running"
        )


    elif estado == "completed":

        clase = "completed"

        texto_estado = "● COMPLETADO"

        clase_estado = (
            "agent-status-completed"
        )


    return f"""
    <div class="agent-card {clase}">

        <div class="agent-icon">
            {icono}
        </div>

        <div class="agent-name">
            {nombre}
        </div>

        <div class="agent-desc">
            {descripcion}
        </div>

        <div class="agent-status {clase_estado}">
            {texto_estado}
        </div>

    </div>
    """


def mostrar_agentes(
    estado="ready"
):

    agentes = [

        (
            "🔧",
            "Especialista mecánico",
            "Analiza síntomas y posibles causas."
        ),

        (
            "📚",
            "Investigador técnico",
            "Consulta la base de conocimiento RAG."
        ),

        (
            "🛡️",
            "Revisor de seguridad",
            "Evalúa riesgos y seguridad de conducción."
        ),

        (
            "🧠",
            "Sintetizador diagnóstico",
            "Integra la evaluación final."
        )
    ]


    columnas = st.columns(
        4
    )


    for columna, agente in zip(
        columnas,
        agentes
    ):

        with columna:

            html(
                tarjeta_agente(
                    agente[0],
                    agente[1],
                    agente[2],
                    estado
                )
            )


# =========================================================
# RIESGO
# =========================================================

def obtener_configuracion_riesgo(
    nivel
):

    nivel = (
        str(nivel)
        .lower()
        .strip()
    )


    if nivel == "alto":

        return {
            "clase": "risk-high",
            "texto": "RIESGO ALTO",
            "icono": "🔴"
        }


    if nivel == "medio":

        return {
            "clase": "risk-medium",
            "texto": "RIESGO MEDIO",
            "icono": "🟠"
        }


    return {
        "clase": "risk-low",
        "texto": "RIESGO BAJO",
        "icono": "🟢"
    }


# =========================================================
# CONDUCCIÓN
# =========================================================

def obtener_texto_conduccion(
    estado
):

    mapa = {

        "seguro":
            "Puede continuar conduciendo.",

        "precaucion":
            "Puede conducir con precaución.",

        "no_recomendado":
            "No es recomendable continuar conduciendo."
    }


    return mapa.get(
        estado,
        "Estado no determinado."
    )


# =========================================================
# LISTAS
# =========================================================

def crear_lista_html(
    elementos
):

    if not elementos:

        return (
            "<div class='empty-info'>"
            "No disponible"
            "</div>"
        )


    items = "".join(
        f"<li>{escape(str(item))}</li>"
        for item in elementos
    )


    return (
        f"<ul class='diagnostic-list'>"
        f"{items}"
        f"</ul>"
    )


# =========================================================
# MOSTRAR DIAGNÓSTICO
# =========================================================

def mostrar_resultado_estructurado(
    resultado
):

    riesgo = (
        obtener_configuracion_riesgo(
            resultado.get(
                "nivel_riesgo",
                "medio"
            )
        )
    )


    sistema = escape(
        str(
            resultado.get(
                "sistema_relacionado",
                "No determinado"
            )
        )
    )


    evaluacion = escape(
        str(
            resultado.get(
                "evaluacion_general",
                "No disponible"
            )
        )
    )


    evidencia = escape(
        str(
            resultado.get(
                "evidencia_tecnica",
                "No disponible"
            )
        )
    )


    fuente = escape(
        str(
            resultado.get(
                "fuente_tecnica",
                "No disponible"
            )
        )
    )


    seguridad = escape(
        str(
            resultado.get(
                "evaluacion_seguridad",
                "No disponible"
            )
        )
    )


    advertencia = escape(
        str(
            resultado.get(
                "advertencia",
                "No disponible"
            )
        )
    )


    conduccion = (
        obtener_texto_conduccion(
            resultado.get(
                "seguridad_conduccion",
                "precaucion"
            )
        )
    )


    causas = (
        crear_lista_html(
            resultado.get(
                "causas_posibles",
                []
            )
        )
    )


    recomendaciones = (
        crear_lista_html(
            resultado.get(
                "recomendaciones",
                []
            )
        )
    )


    revision = (
        "Sí"
        if resultado.get(
            "requiere_revision_profesional",
            False
        )
        else "No"
    )


    html(
        f"""
        <div class="diagnostic-hero">

            <div>

                <div class="diagnostic-label">
                    EVALUACIÓN DEL DIAGNÓSTICO
                </div>

                <div class="diagnostic-system">
                    {sistema}
                </div>

            </div>

            <div class="risk-badge {riesgo['clase']}">

                {riesgo['icono']}
                {riesgo['texto']}

            </div>

        </div>
        """
    )


    html(
        f"""
        <div class="result-card">

            <div class="result-card-title">
                🔎 Evaluación general
            </div>

            <div class="result-card-text">
                {evaluacion}
            </div>

        </div>
        """
    )


    html(
        f"""
        <div class="result-card">

            <div class="result-card-title">
                ⚙️ Posibles causas
            </div>

            <div class="result-card-caption">

                Estas posibilidades son orientativas
                y no representan un diagnóstico confirmado.

            </div>

            {causas}

        </div>
        """
    )


    html(
        f"""
        <div class="result-card technical-card">

            <div class="result-card-title">
                📚 Conocimiento técnico
            </div>

            <div class="technical-source">
                FUENTE / {fuente}
            </div>

            <div class="result-card-text">
                {evidencia}
            </div>

        </div>
        """
    )


    html(
        f"""
        <div class="result-card safety-card">

            <div class="result-card-title">
                🛡️ Evaluación de seguridad
            </div>

            <div class="safety-driving">
                {escape(conduccion)}
            </div>

            <div class="result-card-text">
                {seguridad}
            </div>

            <div class="safety-meta">

                Revisión profesional requerida:

                <strong>
                    {revision}
                </strong>

            </div>

        </div>
        """
    )


    html(
        f"""
        <div class="result-card">

            <div class="result-card-title">
                ✅ Acciones recomendadas
            </div>

            {recomendaciones}

        </div>
        """
    )


    html(
        f"""
        <div class="uncertainty-card">

            <strong>
                ℹ️ Limitaciones del diagnóstico
            </strong>

            <div>
                {advertencia}
            </div>

        </div>
        """
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:


    html(
        """
        <div class="brand-title">

            AutoDiag AI

            <span class="brand-version">
                V4
            </span>

        </div>

        <div class="brand-subtitle">
            Asistente de diagnóstico automotriz
        </div>
        """
    )


    pagina = st.radio(

        "Navegación",

        [
            "🚗 Nuevo diagnóstico",
            "🕘 Historial de diagnósticos",
            "🔧 Mantenimiento",
            "📚 Conocimiento técnico",
            "⚙️ Configuración"
        ],

        label_visibility="collapsed"
    )

    mostrar_usuario_sidebar(usuario_actual)


    st.divider()


    html(
        """
        <div class="status-online">

            <span class="status-dot"></span>

            SISTEMA DE IA EN LÍNEA

        </div>

        <div style="
            color:#64748B;
            font-size:0.72rem;
            margin-top:0.6rem;
        ">

            4 agentes especialistas disponibles

        </div>
        """
    )


# =========================================================
# NUEVO DIAGNÓSTICO
# =========================================================

if pagina == "🚗 Nuevo diagnóstico":


    html(
        """
        <div class="page-kicker">
            AUTODIAG / DIAGNÓSTICO
        </div>

        <div class="page-title">
            Diagnóstico automotriz
        </div>

        <div class="page-subtitle">

            Describe lo que está ocurriendo con tu vehículo.

            AutoDiag AI analizará los síntomas utilizando
            especialistas de inteligencia artificial
            y conocimiento técnico automotriz.

        </div>
        """
    )


    html(
        """
        <div class="diag-card">

            <div class="card-title">
                Datos del vehículo
            </div>

            <div class="card-caption">

                Esta información es opcional,
                pero permite entregar mayor contexto.

            </div>

        </div>
        """
    )


    (
        col_marca,
        col_modelo,
        col_anio,
        col_motor,
        col_km
    ) = st.columns(5)


    with col_marca:

        marca = st.text_input(
            "Marca",
            placeholder="Peugeot"
        )


    with col_modelo:

        modelo = st.text_input(
            "Modelo",
            placeholder="3008"
        )


    with col_anio:

        anio = st.text_input(
            "Año",
            placeholder="2025"
        )


    with col_motor:

        motor = st.text_input(
            "Motor",
            placeholder="1.2 PureTech"
        )


    with col_km:

        kilometraje = st.text_input(
            "Kilometraje",
            placeholder="24.500 km"
        )


    st.write("")


    html(
        """
        <div class="diag-card">

            <div class="card-title">
                ¿Qué está ocurriendo con tu vehículo?
            </div>

            <div class="card-caption">

                Describe los síntomas con el mayor detalle posible.

                AutoDiag AI está limitado exclusivamente
                a consultas automotrices.

            </div>

        </div>
        """
    )


    with st.form(
        "formulario_diagnostico"
    ):


        consulta = st.text_area(

            "Síntomas",

            placeholder=(
                "Ejemplo: cuando freno siento una vibración "
                "y el volante tiembla..."
            ),

            height=160,

            label_visibility="collapsed"
        )


        analizar = (
            st.form_submit_button(
                "⚡ Analizar vehículo",
                use_container_width=True
            )
        )


    st.subheader(
        "Equipo de especialistas de IA"
    )


    placeholder_agentes = (
        st.empty()
    )


    with placeholder_agentes.container():

        if (
            st.session_state
            .diagnostico_ejecutado
        ):

            mostrar_agentes(
                "completed"
            )

        else:

            mostrar_agentes(
                "ready"
            )


    # =====================================================
    # ANALIZAR
    # =====================================================

    if analizar:


        if not consulta.strip():


            st.warning(
                "Debes describir al menos un síntoma."
            )


        else:


            datos_vehiculo = []


            if marca.strip():

                datos_vehiculo.append(
                    f"Marca: {marca.strip()}"
                )


            if modelo.strip():

                datos_vehiculo.append(
                    f"Modelo: {modelo.strip()}"
                )


            if anio.strip():

                datos_vehiculo.append(
                    f"Año: {anio.strip()}"
                )


            if motor.strip():

                datos_vehiculo.append(
                    f"Motor: {motor.strip()}"
                )


            if kilometraje.strip():

                datos_vehiculo.append(
                    f"Kilometraje: {kilometraje.strip()}"
                )


            consulta_completa = (
                consulta.strip()
            )


            if datos_vehiculo:

                consulta_completa = (

                    "Información del vehículo:\n"

                    + " | ".join(
                        datos_vehiculo
                    )

                    + "\n\nSíntomas reportados:\n"

                    + consulta.strip()
                )


            try:

                # =========================================
                # VALIDACIÓN ANTES DE CAMBIAR LA UI
                # =========================================

                validar_consulta_automotriz(
                    consulta_completa
                )


                evaluacion_critica = (
                    evaluar_seguridad_critica(
                        consulta_completa
                    )
                )


                # =========================================
                # ALERTA CRÍTICA PREVIA
                # =========================================

                if evaluacion_critica[
                    "es_critico"
                ]:

                    titulos_alertas = ", ".join(

                        alerta[
                            "titulo"
                        ]

                        for alerta in evaluacion_critica[
                            "alertas"
                        ]
                    )


                    st.error(
                        "⚠️ Se detectó una señal "
                        "potencialmente crítica: "
                        f"{titulos_alertas}."
                    )


                    st.warning(
                        "Por seguridad, AutoDiag AI "
                        "no permitirá que el diagnóstico "
                        "final clasifique esta situación "
                        "por debajo de riesgo alto."
                    )


                # =========================================
                # AGENTES ANALIZANDO
                # =========================================

                placeholder_agentes.empty()


                with (
                    placeholder_agentes
                    .container()
                ):

                    mostrar_agentes(
                        "running"
                    )


                # =========================================
                # CREWAI
                # =========================================

                with st.spinner(
                    "AutoDiag AI está analizando el vehículo..."
                ):


                    resultado = (
                        ejecutar_diagnostico(
                            consulta_completa
                        )
                    )


                # =========================================
                # GUARDAR SESIÓN
                # =========================================

                st.session_state.resultado_diagnostico = (
                    resultado
                )


                st.session_state.diagnostico_ejecutado = (
                    True
                )


                st.session_state.ultimo_vehiculo = {

                    "marca":
                        marca.strip(),

                    "modelo":
                        modelo.strip(),

                    "anio":
                        anio.strip(),

                    "motor":
                        motor.strip(),

                    "kilometraje":
                        kilometraje.strip()
                }


                st.session_state.ultimo_sintoma = (
                    consulta.strip()
                )


                st.session_state.diagnostico_guardado_id = (
                    None
                )


                st.session_state.confirmar_email = (
                    False
                )


                placeholder_agentes.empty()


                with (
                    placeholder_agentes
                    .container()
                ):

                    mostrar_agentes(
                        "completed"
                    )


            # =================================================
            # CONSULTA FUERA DE DOMINIO
            # =================================================

            except ConsultaFueraDeDominioError as error:


                st.session_state.diagnostico_ejecutado = (
                    False
                )


                placeholder_agentes.empty()


                with (
                    placeholder_agentes
                    .container()
                ):

                    mostrar_agentes(
                        "ready"
                    )


                st.warning(
                    "🚗 Consulta fuera del ámbito de AutoDiag AI"
                )


                st.info(
                    str(error)
                )


            # =================================================
            # OTROS ERRORES
            # =================================================

            except Exception as error:


                st.session_state.diagnostico_ejecutado = (
                    False
                )


                placeholder_agentes.empty()


                with (
                    placeholder_agentes
                    .container()
                ):

                    mostrar_agentes(
                        "ready"
                    )


                st.error(
                    "No fue posible completar el diagnóstico."
                )


                with st.expander(
                    "Ver detalles técnicos"
                ):

                    st.code(
                        str(error)
                    )


    # =====================================================
    # RESULTADO
    # =====================================================

    if (
        st.session_state
        .resultado_diagnostico
    ):


        mostrar_resultado_estructurado(
            st.session_state
            .resultado_diagnostico
        )


        st.write("")


        (
            col_nuevo,
            col_guardar,
            col_email
        ) = st.columns(3)


        # =================================================
        # NUEVO
        # =================================================

        with col_nuevo:


            if st.button(
                "＋ Nuevo diagnóstico",
                use_container_width=True
            ):


                st.session_state.resultado_diagnostico = None

                st.session_state.diagnostico_ejecutado = False

                st.session_state.ultimo_vehiculo = {}

                st.session_state.ultimo_sintoma = ""

                st.session_state.diagnostico_guardado_id = None

                st.session_state.confirmar_email = False

                st.rerun()


        # =================================================
        # GUARDAR
        # =================================================

        with col_guardar:


            if (
                st.session_state
                .diagnostico_guardado_id
                is None
            ):


                guardar = st.button(
                    "💾 Guardar informe",
                    use_container_width=True
                )


                if guardar:


                    vehiculo = (
                        st.session_state
                        .ultimo_vehiculo
                    )


                    diagnostico_id = (
                        guardar_diagnostico(

                            consulta=(
                                st.session_state
                                .ultimo_sintoma
                            ),

                            resultado=(
                                st.session_state
                                .resultado_diagnostico
                            ),

                            marca=vehiculo.get(
                                "marca",
                                ""
                            ),

                            modelo=vehiculo.get(
                                "modelo",
                                ""
                            ),

                            anio=vehiculo.get(
                                "anio",
                                ""
                            ),

                            motor=vehiculo.get(
                                "motor",
                                ""
                            ),

                            kilometraje=vehiculo.get(
                                "kilometraje",
                                ""
                            ),

                            session_token=st.session_state.auth_token
                        )
                    )


                    st.session_state.diagnostico_guardado_id = (
                        diagnostico_id
                    )


                    st.success(
                        "Informe guardado correctamente "
                        f"· #{diagnostico_id}"
                    )


            else:


                st.button(
                    "✅ Informe guardado",
                    disabled=True,
                    use_container_width=True
                )


        # =================================================
        # EMAIL
        # =================================================

        with col_email:


            if st.button(
                "✉️ Enviar por correo",
                use_container_width=True
            ):


                st.session_state.confirmar_email = (
                    True
                )


        # =================================================
        # CONFIRMACIÓN EMAIL
        # =================================================

        if (
            st.session_state
            .confirmar_email
        ):


            st.write("")


            try:


                destino_email = (
                    obtener_correo_destino()
                )


                st.warning(
                    "Estás a punto de enviar este informe "
                    f"a {destino_email}."
                )


                (
                    col_confirmar,
                    col_cancelar
                ) = st.columns(2)


                with col_confirmar:


                    confirmar_envio = (
                        st.button(
                            "✅ Confirmar envío",
                            use_container_width=True
                        )
                    )


                with col_cancelar:


                    cancelar_envio = (
                        st.button(
                            "Cancelar",
                            use_container_width=True
                        )
                    )


                if cancelar_envio:


                    st.session_state.confirmar_email = (
                        False
                    )

                    st.rerun()


                if confirmar_envio:


                    try:


                        with st.spinner(
                            "Enviando informe por Gmail..."
                        ):


                            respuesta_email = (
                                enviar_informe_gmail(

                                    resultado=(
                                        st.session_state
                                        .resultado_diagnostico
                                    ),

                                    vehiculo=(
                                        st.session_state
                                        .ultimo_vehiculo
                                    ),

                                    sintoma=(
                                        st.session_state
                                        .ultimo_sintoma
                                    )
                                )
                            )


                        st.session_state.confirmar_email = (
                            False
                        )


                        st.success(
                            "✅ Informe enviado correctamente "
                            f"a {respuesta_email['destino']}."
                        )


                    except Exception as error:


                        st.error(
                            "No fue posible enviar el correo."
                        )


                        with st.expander(
                            "Ver detalles técnicos"
                        ):

                            st.code(
                                str(error)
                            )


            except Exception as error:


                st.error(
                    str(error)
                )


# =========================================================
# HISTORIAL
# =========================================================

elif pagina == "🕘 Historial de diagnósticos":


    html(
        """
        <div class="page-kicker">
            AUTODIAG / HISTORIAL
        </div>

        <div class="page-title">
            Historial de diagnósticos
        </div>

        <div class="page-subtitle">

            Consulta los informes guardados anteriormente
            y vuelve a abrir sus evaluaciones completas.

        </div>
        """
    )


    diagnosticos = (
        listar_diagnosticos(
            session_token=st.session_state.auth_token,
        )
    )


    if not diagnosticos:


        st.info(
            "Todavía no existen diagnósticos guardados."
        )


    else:


        filas = []


        for diagnostico in diagnosticos:


            vehiculo = " ".join(

                parte

                for parte in [

                    diagnostico.get(
                        "marca",
                        ""
                    ),

                    diagnostico.get(
                        "modelo",
                        ""
                    ),

                    diagnostico.get(
                        "anio",
                        ""
                    )
                ]

                if parte
            )


            filas.append(
                {

                    "ID":
                        diagnostico["id"],

                    "Fecha":
                        diagnostico["fecha"],

                    "Vehículo":
                        vehiculo
                        or "No especificado",

                    "Sistema":
                        diagnostico.get(
                            "sistema",
                            ""
                        ),

                    "Riesgo":
                        diagnostico.get(
                            "riesgo",
                            ""
                        )
                }
            )


        st.dataframe(
            filas,
            use_container_width=True,
            hide_index=True
        )


        st.write("")


        opciones = {}


        for diagnostico in diagnosticos:


            vehiculo = " ".join(

                parte

                for parte in [

                    diagnostico.get(
                        "marca",
                        ""
                    ),

                    diagnostico.get(
                        "modelo",
                        ""
                    )
                ]

                if parte
            )


            if not vehiculo:

                vehiculo = (
                    "Vehículo no especificado"
                )


            etiqueta = (

                f"#{diagnostico['id']} · "
                f"{vehiculo} · "
                f"{diagnostico.get('sistema', '')} · "
                f"{diagnostico.get('riesgo', '')}"
            )


            opciones[
                etiqueta
            ] = diagnostico[
                "id"
            ]


        seleccion = st.selectbox(
            "Selecciona un informe",
            list(
                opciones.keys()
            )
        )


        diagnostico_id = (
            opciones[
                seleccion
            ]
        )


        if st.button(
            "📄 Abrir informe"
        ):


            st.session_state.historial_abierto_id = (
                diagnostico_id
            )


        if (
            st.session_state
            .historial_abierto_id
            is not None
        ):


            diagnostico = (
                obtener_diagnostico(
                    st.session_state
                    .historial_abierto_id,
                    session_token=st.session_state.auth_token,
                )
            )


            if diagnostico:


                st.divider()


                datos_vehiculo_historial = " ".join(

                    parte

                    for parte in [

                        str(
                            diagnostico.get(
                                "marca",
                                ""
                            )
                        ),

                        str(
                            diagnostico.get(
                                "modelo",
                                ""
                            )
                        ),

                        str(
                            diagnostico.get(
                                "anio",
                                ""
                            )
                        )
                    ]

                    if parte
                )


                html(
                    f"""
                    <div class="diag-card">

                        <div class="card-title">
                            Datos del vehículo
                        </div>

                        <div class="card-caption">

                            {
                                escape(
                                    datos_vehiculo_historial
                                )
                            }

                            <br>

                            {
                                escape(
                                    str(
                                        diagnostico.get(
                                            "motor",
                                            ""
                                        )
                                    )
                                )
                            }

                            <br>

                            {
                                escape(
                                    str(
                                        diagnostico.get(
                                            "kilometraje",
                                            ""
                                        )
                                    )
                                )
                            }

                        </div>

                    </div>
                    """
                )


                html(
                    f"""
                    <div class="result-card">

                        <div class="result-card-title">
                            📝 Síntoma reportado
                        </div>

                        <div class="result-card-text">

                            {
                                escape(
                                    str(
                                        diagnostico.get(
                                            "consulta",
                                            ""
                                        )
                                    )
                                )
                            }

                        </div>

                    </div>
                    """
                )


                mostrar_resultado_estructurado(
                    diagnostico[
                        "resultado"
                    ]
                )


# =========================================================
# MANTENIMIENTO
# =========================================================

elif pagina == "🔧 Mantenimiento":


    html(
        """
        <div class="page-kicker">
            AUTODIAG / MANTENIMIENTO
        </div>

        <div class="page-title">
            Mantenimiento preventivo
        </div>

        <div class="page-subtitle">

            Consulta recomendaciones preventivas
            para diferentes sistemas del vehículo.

        </div>
        """
    )


    categorias = (
        obtener_categorias_mantenimiento()
    )


    categoria = st.selectbox(

        "Selecciona un sistema",

        categorias,

        format_func=(
            obtener_nombre_categoria
        )
    )


    datos_mantenimiento = (
        obtener_mantenimiento(
            categoria
        )
    )


    html(
        f"""
        <div class="diagnostic-hero">

            <div>

                <div class="diagnostic-label">
                    SISTEMA SELECCIONADO
                </div>

                <div class="diagnostic-system">

                    {
                        escape(
                            datos_mantenimiento[
                                "nombre"
                            ]
                        )
                    }

                </div>

            </div>

            <div class="risk-badge risk-low">
                🔧 MANTENIMIENTO
            </div>

        </div>
        """
    )


    recomendaciones_html = (
        crear_lista_html(
            datos_mantenimiento[
                "recomendaciones"
            ]
        )
    )


    html(
        f"""
        <div class="result-card">

            <div class="result-card-title">
                ✅ Recomendaciones preventivas
            </div>

            {recomendaciones_html}

        </div>
        """
    )


    html(
        """
        <div class="uncertainty-card">

            <strong>
                ℹ️ Importante
            </strong>

            <div>

                Los intervalos exactos dependen
                del fabricante, modelo, motorización,
                kilometraje y condiciones de uso.

            </div>

        </div>
        """
    )


# =========================================================
# CONOCIMIENTO TÉCNICO
# =========================================================

elif pagina == "📚 Conocimiento técnico":


    html(
        """
        <div class="page-kicker">
            AUTODIAG / CONOCIMIENTO
        </div>

        <div class="page-title">
            Conocimiento técnico
        </div>

        <div class="page-subtitle">

            Consulta directamente la base técnica
            utilizada por AutoDiag AI.

        </div>
        """
    )


    html(
        """
        <div class="diag-card">

            <div class="card-title">
                📚 Base técnica AutoDiag
            </div>

            <div class="card-caption">

                Esta búsqueda utiliza embeddings
                semánticos y ChromaDB.

                No utiliza Groq y está limitada
                al dominio automotriz.

            </div>

        </div>
        """
    )


    with st.form(
        "formulario_conocimiento"
    ):


        consulta_tecnica = st.text_area(

            "Consulta técnica",

            placeholder=(
                "Ejemplo: ¿Qué puede provocar "
                "tirones y pérdida de potencia?"
            ),

            height=130
        )


        cantidad = st.slider(

            "Cantidad de documentos",

            min_value=1,

            max_value=4,

            value=3
        )


        buscar = (
            st.form_submit_button(
                "🔎 Buscar información técnica",
                use_container_width=True
            )
        )


    # =====================================================
    # BUSCAR RAG
    # =====================================================

    if buscar:


        if not consulta_tecnica.strip():


            st.warning(
                "Escribe una consulta antes de buscar."
            )


        else:


            try:

                # =========================================
                # GUARDRAIL TAMBIÉN PARA RAG
                # =========================================

                validar_consulta_automotriz(
                    consulta_tecnica
                )


                with st.spinner(
                    "Buscando en la base de conocimiento..."
                ):


                    resultados = (
                        buscar_documentos_vectoriales(
                            consulta=consulta_tecnica,
                            cantidad=cantidad
                        )
                    )


                st.session_state.resultados_conocimiento = (
                    resultados
                )


                st.session_state.consulta_conocimiento = (
                    consulta_tecnica.strip()
                )


            except ConsultaFueraDeDominioError as error:


                st.session_state.resultados_conocimiento = []

                st.session_state.consulta_conocimiento = ""


                st.warning(
                    "🚗 Consulta fuera del ámbito "
                    "de conocimiento de AutoDiag AI."
                )


                st.info(
                    str(error)
                )


            except Exception as error:


                st.error(
                    "No fue posible consultar "
                    "la base de conocimiento."
                )


                with st.expander(
                    "Ver detalles técnicos"
                ):

                    st.code(
                        str(error)
                    )


    # =====================================================
    # RESULTADOS RAG
    # =====================================================

    if (
        st.session_state
        .resultados_conocimiento
    ):


        st.write("")


        html(
            f"""
            <div class="diagnostic-hero">

                <div>

                    <div class="diagnostic-label">
                        CONSULTA TÉCNICA
                    </div>

                    <div style="
                        color:#F8FAFC;
                        font-size:1rem;
                        font-weight:600;
                        margin-top:0.4rem;
                    ">

                        {
                            escape(
                                st.session_state
                                .consulta_conocimiento
                            )
                        }

                    </div>

                </div>

                <div class="risk-badge risk-low">
                    📚 RAG
                </div>

            </div>
            """
        )


        html(
            """
            <div class="uncertainty-card">

                <strong>
                    ℹ️ Sobre los resultados
                </strong>

                <div>

                    El orden representa relevancia semántica,
                    no una probabilidad de diagnóstico.

                </div>

            </div>
            """
        )


        for indice, resultado in enumerate(
            st.session_state
            .resultados_conocimiento,
            start=1
        ):


            categoria = escape(
                str(
                    resultado.get(
                        "categoria",
                        "Sin categoría"
                    )
                )
            )


            subcategoria = escape(
                str(
                    resultado.get(
                        "subcategoria",
                        "General"
                    )
                )
            )


            fuente = escape(
                str(
                    resultado.get(
                        "fuente",
                        "No disponible"
                    )
                )
            )


            contenido = escape(
                str(
                    resultado.get(
                        "contenido",
                        ""
                    )
                )
            )


            html(
                f"""
                <div class="result-card technical-card">

                    <div class="result-card-title">
                        📄 Resultado técnico {indice}
                    </div>

                    <div class="technical-source">

                        CATEGORÍA / {categoria}

                        <br>

                        SUBCATEGORÍA / {subcategoria}

                        <br>

                        FUENTE / {fuente}

                    </div>

                    <div class="result-card-text">
                        {contenido}
                    </div>

                </div>
                """
            )


# =========================================================
# CONFIGURACIÓN
# =========================================================

elif pagina == "⚙️ Configuración":


    html(
        """
        <div class="page-kicker">
            AUTODIAG / CONFIGURACIÓN
        </div>

        <div class="page-title">
            Configuración
        </div>

        <div class="page-subtitle">
            Estado general de AutoDiag AI V4.
        </div>
        """
    )


    # =====================================================
    # GMAIL
    # =====================================================

    try:


        correo = (
            obtener_correo_destino()
        )


        st.success(
            "📧 Gmail configurado correctamente "
            f"para: {correo}"
        )


    except Exception:


        st.warning(
            "Gmail todavía no está configurado."
        )


    # =====================================================
    # RAG
    # =====================================================

    try:


        info_rag = (
            obtener_info_base()
        )


        html(
            f"""
            <div class="result-card">

                <div class="result-card-title">
                    📚 Base de conocimiento
                </div>

                <div class="result-card-text">

                    Versión:
                    <strong>
                        {
                            escape(
                                info_rag[
                                    "version"
                                ]
                            )
                        }
                    </strong>

                    <br>

                    Documentos:
                    <strong>
                        {
                            info_rag[
                                "documentos"
                            ]
                        }
                    </strong>

                    <br>

                    Fragmentos:
                    <strong>
                        {
                            info_rag[
                                "fragmentos"
                            ]
                        }
                    </strong>

                    <br><br>

                    Motor de búsqueda:
                    embeddings semánticos + ChromaDB.

                </div>

            </div>
            """
        )


    except Exception:


        st.warning(
            "No fue posible obtener información del RAG."
        )


    # =====================================================
    # SEGURIDAD
    # =====================================================

    html(
        """
        <div class="result-card">

            <div class="result-card-title">
                🔒 Guardrail de dominio
            </div>

            <div class="result-card-text">

                Estado:
                <strong>ACTIVO</strong>

                <br><br>

                Las consultas que no presentan suficiente
                contexto automotriz son rechazadas antes
                de iniciar los agentes o consultar el RAG.

            </div>

        </div>
        """
    )


    html(
        """
        <div class="result-card safety-card">

            <div class="result-card-title">
                🛡️ Safety Guard
            </div>

            <div class="result-card-text">

                Estado:
                <strong>ACTIVO</strong>

                <br><br>

                AutoDiag AI analiza localmente señales
                críticas antes de ejecutar los agentes.

                <br><br>

                Cuando se detecta una condición crítica,
                el resultado final no puede reducirse
                por debajo de riesgo alto, se marca
                la conducción como no recomendada
                y se exige revisión profesional.

            </div>

        </div>
        """
    )
