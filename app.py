import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64
import random

st.set_page_config(page_title="Narrador de Partido ⚽", page_icon="⚽", layout="centered")

st.title("🎙️ Narrador de Partido de Fútbol")

# Imagen decorativa (asegúrate de tener futbol.jpg o cambia el nombre)
try:
    image = Image.open('futbol.jpeg')
    st.image(image, width=350)
except:
    st.warning("Agrega una imagen llamada 'futbol.jpg' en tu carpeta para mostrarla aquí ⚽")

# Sidebar
with st.sidebar:
    st.subheader("⚽ Opciones de Narrador")
    st.write("Selecciona el modo de narración:")
    modo = st.radio("Modo:", ["Narrador Automático", "Narración Escrita"])

# Crear carpeta temporal
os.makedirs("temp", exist_ok=True)

# -----------------------------------
# 🏟️ MODO AUTOMÁTICO
# -----------------------------------
if modo == "Narrador Automático":
    st.header("🎧 Narrador Automático")

    equipo1 = st.text_input("Equipo Local:", "Real Madrid")
    equipo2 = st.text_input("Equipo Visitante:", "Barcelona")

    minuto = random.randint(1, 90)
    jugador = random.choice(["Vinícius Jr", "Lewandowski", "Bellingham", "Pedri", "Rodrygo", "Gavi", "Modric"])
    accion = random.choice([
        "avanza con el balón por la banda izquierda",
        "lanza un disparo potente desde fuera del área",
        "mete un pase filtrado impresionante",
        "realiza una jugada individual espectacular",
        "manda un centro preciso al corazón del área"
    ])

    if st.button("🎙️ Generar narración automática"):
        narracion = (
            f"¡Bienvenidos al gran partido entre {equipo1} y {equipo2}! "
            f"Estamos en el minuto {minuto}, el marcador sigue igualado... "
            f"¡Atención! {jugador} {accion}... "
            f"¡GOOOOOOOL de {equipo1 if random.random() > 0.5 else equipo2}! "
            f"El estadio estalla en emoción, qué momento increíble del partido."
        )

        st.subheader("🗣️ Narración generada:")
        st.write(narracion)

        tts = gTTS(narracion, lang='es')
        filename = f"temp/narracion_auto_{int(time.time())}.mp3"
        tts.save(filename)

        audio_file = open(filename, "rb")
        st.audio(audio_file.read(), format="audio/mp3")

        # Descargar audio
        def get_download_link(file_path, label="⬇️ Descargar narración"):
            with open(file_path, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{label}</a>'
            return href

        st.markdown(get_download_link(filename), unsafe_allow_html=True)

# -----------------------------------
# ✍️ MODO ESCRITO POR EL USUARIO
# -----------------------------------
else:
    st.header("📝 Escribe tu propia narración")

    texto_usuario = st.text_area("Escribe aquí tu narración de fútbol:", 
                                 placeholder="Ejemplo: Minuto 89, el balón lo tiene Messi... se perfila, dispara... ¡GOLAZO!")

    idioma = st.selectbox("Selecciona el idioma:", ["Español", "English"])
    lang_code = "es" if idioma == "Español" else "en"

    if st.button("🎧 Convertir mi narración a audio"):
        if texto_usuario.strip() == "":
            st.error("⚠️ Por favor escribe algo antes de convertirlo a audio.")
        else:
            tts = gTTS(texto_usuario, lang=lang_code)
            filename = f"temp/narracion_manual_{int(time.time())}.mp3"
            tts.save(filename)

            audio_file = open(filename, "rb")
            st.audio(audio_file.read(), format="audio/mp3")

            # Descargar audio
            def get_download_link(file_path, label="⬇️ Descargar narración"):
                with open(file_path, "rb") as f:
                    data = f.read()
                b64 = base64.b64encode(data).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{label}</a>'
                return href

            st.markdown(get_download_link(filename), unsafe_allow_html=True)

# -----------------------------------
# 🧹 Limpieza de archivos antiguos
# -----------------------------------
def remove_old_files(days=1):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    for f in mp3_files:
        if os.stat(f).st_mtime < now - days * 86400:
            os.remove(f)

remove_old_files(1)

