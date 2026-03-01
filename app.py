import streamlit as st
import yt_dlp
import os

# הגדרות דף ועיצוב קשוח
st.set_page_config(page_title="YT-COMMANDER", page_icon="💀", layout="centered")

# CSS לעיצוב אישי - שחור וכתום
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ff4b4b; }
    .stTextInput>div>div>input { background-color: #1a1c24; color: #00ff00; border: 1px solid #ff4b4b; }
    .stButton>button { width: 100%; border-radius: 0px; background-color: #ff4b4b; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ff0000; border: 1px solid white; }
    h1 { color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px #000000; }
    </style>
    """, unsafe_allow_index=True)

st.title("💀 YT-AUDIO COMMANDER")
st.write("---")

# קלט
url = st.text_input("ENTER TARGET URL:", placeholder="https://youtube.com/...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("SELECT MISSION:", ["Download Only", "Download & Transcribe"])
with col2:
    quality = st.select_slider("AUDIO BITRATE:", options=["128", "192", "320"], value="192")

if url:
    if st.button("EXECUTE"):
        try:
            with st.status("🛠️ PROCESSING DATA...", expanded=True) as status:
                st.write("Extracting audio stream...")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality,
                    }],
                    'outtmpl': 'mission_audio.%(ext)s',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio_file')
                
                st.write("System: Audio ready.")
                
                if action == "Download & Transcribe":
                    st.warning("Transcribing... (Note: This requires a Transcription API setup like Groq)")
                    # כאן אפשר להוסיף את הקריאה ל-Groq API כמו בסרטון של שחר
                
                status.update(label="MISSION ACCOMPLISHED", state="complete")

            with open("mission_audio.mp3", "rb") as f:
                st.audio(f.read())
                st.download_button(label="📥 DOWNLOAD MP3", data=f, file_name=f"{title}.mp3")
            
            os.remove("mission_audio.mp3")
            
        except Exception as e:
            st.error(f"SYSTEM FAILURE: {e}")

st.write("---")
st.caption("STATUS: ENCRYPTED | OPERATOR: BOSS")
