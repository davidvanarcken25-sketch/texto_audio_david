import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64
import random

st.set_page_config(page_title="Narrador de Partido ⚽", page_icon="⚽")

st.title("🎙️ Narrador de Partido de Fútbol")

image = Image.open('futbol.jpeg')  # Usa una imagen de fútbol en tu carpeta
st.image(image, width=350)

with st.sidebar:
    st.subheader("⚽ Crea una narración de partido con voz")
    st.write("Selecciona los equipos, genera el relato y escucha la narración.")

# --- Crear carpeta temporal ---
try:
    os.mkdir("temp")
except:
    pass

# --- Opciones del usuario ---
equipo1 = st.text_input("🏟️ Equipo Local:", "Real Madrid")
equipo2 = st.text_input("🌍 Equipo Visitante:", "Barcelona")

minuto = random.randint(1, 90)
jugador = random.choice(["Vinícius Jr", "Lewandowski", "Bellingham", "Pedri", "Rodrygo", "Gavi", "Modric"])
accion = random.choice([
    "avanza con el balón por la banda izquierda",
    "mete un pase filtrado impresionante",
    "lanza un disparo potente desde fuera del área",
    "realiza una jugada individual espectacular",
    "manda un centro preciso al corazón del área"
])

# --- Generar narración ---
if st.button("🎙️ Generar narración"):
    narracion = (
        f"¡Bienvenidos al gran partido entre {equipo1} y {equipo2}! "
        f"Estamos en el minuto {minuto}, el marcador sigue igualado... "
        f"¡Atención! {jugador} {accion}... "
        f"¡GOOOOOOOL de {equipo1 if random.random() > 0.5 else equipo2}! "
        f"El estadio estalla en emoción, qué momento increíble del partido."
    )

    st.subheader("🗣️ Narración generada:")
    st.write(narracion)

    # --- Convertir texto a audio ---
    tts = gTTS(narracion, lang='es')
    filename = f"temp/narracion_{int(time.time())}.mp3"
    tts.save(filename)

    # --- Reproducir audio ---
    audio_file = open(filename, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

    # --- Botón de descarga ---
    def get_download_link(file_path, label="Descargar narración"):
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{label}</a>'
        return href

    st.markdown(get_download_link(filename), unsafe_allow_html=True)

# --- Limpieza de archivos antiguos ---
def remove_old_files(days=1):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    for f in mp3_files:
        if os.stat(f).st_mtime < now - days * 86400:
            os.remove(f)

remove_old_files(1)
