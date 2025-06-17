import streamlit as st
import groq

# ----- CONFIGURACIONES DISPONIBLES -----
temas = ['Atardecer', 'Noche', 'Mar']
modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

# ----- CONFIGURAR PÁGINA -----
st.set_page_config(page_title="RoboAlfred", page_icon="🤖", layout="wide")

# ----- SIDEBAR -----
with st.sidebar:
    st.title("⚙️ Configuración")
    modelo_seleccionado = st.selectbox("Modelo AI:", modelos)
    tema_seleccionado = st.selectbox("Tema visual:", temas)
    font_size = st.slider("Tamaño de fuente", 12, 24, 16)
    if st.button("🧹 Limpiar historial"):
        st.session_state.mensajes = []
        st.experimental_rerun()

# ----- APLICAR TEMA VISUAL -----
def aplicar_tema(tema, font_size):
    if tema == "Noche":
        bg_color = "#0b0c10"
        text_color = "#66fcf1"
        chat_bg = "#1f2833"
        border_color = "#45a29e"
        input_bg = "#12192b"
        input_text = "#a3f0f5"
    elif tema == "Mar":
        bg_color = "#d0f0fd"
        text_color = "#03396c"
        chat_bg = "#b6e0fe"
        border_color = "#005b96"
        input_bg = "#c0ddff"
        input_text = "#002855"
    else:  # Atardecer
        bg_color = "#fbe8a6"
        text_color = "#bb5500"
        chat_bg = "#ffd97d"
        border_color = "#cc7000"
        input_bg = "#fff2cc"
        input_text = "#7a3e00"

    st.markdown(f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
            font-size: {font_size}px;
        }}
        .chat-card {{
            background-color: {chat_bg};
            border-left: 5px solid {border_color};
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 10px;
        }}
        .stButton>button {{
            background-color: {border_color} !important;
            color: white !important;
            border-radius: 8px !important;
        }}
        textarea, input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-radius: 8px !important;
        }}
        .main {{
            background-color: {bg_color};
            color: {text_color};
        }}
    </style>
    """, unsafe_allow_html=True)

aplicar_tema(tema_seleccionado, font_size)

# ----- FUNCIONES -----

def crear_cliente_groq():
    if "GROQ_API_KEY" not in st.secrets:
        st.error("❌ Falta GROQ_API_KEY en .streamlit/secrets.toml")
        st.stop()
    return groq.Groq(api_key=st.secrets["GROQ_API_KEY"])

def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

def agregar_mensaje(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

# ✅ ESTA ES LA FUNCIÓN QUE PROVOCABA EL ERROR, DEBE IR ANTES DE USARSE
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=False
    )
    return respuesta.choices[0].message.content

# ----- EJECUCIÓN PRINCIPAL -----
def ejecutar_chat():
    cliente = crear_cliente_groq()
    inicializar_estado_chat()
    obtener_mensajes_previos()

    mensaje_usuario = st.chat_input("Envia tu mensaje")
    if mensaje_usuario:
        agregar_mensaje("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        respuesta = obtener_respuesta_modelo(cliente, modelo_seleccionado, st.session_state.mensajes)
        agregar_mensaje("assistant", respuesta)
        mostrar_mensaje("assistant", respuesta)

# ----- INICIO DE LA APP -----
if __name__ == '__main__':
    ejecutar_chat()