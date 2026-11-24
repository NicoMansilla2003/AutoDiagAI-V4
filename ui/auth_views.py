import streamlit as st

from services.auth_service import AuthError, login, register_user


def mostrar_acceso() -> None:
    st.title("AutoDiag AI V4")
    st.subheader("Ingresa o crea tu cuenta")
    entrar, crear = st.tabs(["Iniciar sesión", "Crear cuenta"])

    with entrar:
        with st.form("auth_login"):
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Iniciar sesión", use_container_width=True)
        if submitted:
            try:
                _, token = login(email, password)
                st.session_state.auth_token = token
                st.rerun()
            except AuthError as error:
                st.error(str(error))

    with crear:
        with st.form("auth_register"):
            name = st.text_input("Nombre")
            email = st.text_input("Correo electrónico", key="register_email")
            password = st.text_input("Contraseña (12 a 128 caracteres)", type="password", key="register_password")
            confirm = st.text_input("Confirma la contraseña", type="password", key="register_confirm")
            submitted = st.form_submit_button("Crear cuenta", use_container_width=True)
        if submitted:
            try:
                _, token = register_user(name, email, password, confirm)
                st.session_state.auth_token = token
                st.success("Cuenta creada.")
                st.rerun()
            except AuthError as error:
                st.error(str(error))


def mostrar_usuario_sidebar(user: dict) -> None:
    st.sidebar.divider()
    st.sidebar.caption(f"{user['display_name']} · {user['email']}")
    if user["role"] == "admin":
        st.sidebar.caption("Administrador")
    if st.sidebar.button("Cerrar sesión", use_container_width=True):
        from services.auth_service import logout

        logout(st.session_state.get("auth_token"))
        st.session_state.pop("auth_token", None)
        st.session_state.pop("historial_abierto_id", None)
        st.rerun()
