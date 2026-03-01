import streamlit as st
import yt_dlp
import os

# הגדרות דף
st.set_page_config(page_title="YT-COMMANDER", page_icon="💀", layout="centered")

# CSS מתוקן לעיצוב האקרים
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #ff4b4b; text-align: center; font-family: 'Courier New', Courier, monospace; }
    .stTextInput label { color: #ff4b4b !important; }
    .stButton>button { 
        background-color: #ff4b4b; 
        color: white; 
        border-radius: 0px; 
        border: 1px solid white;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button:hover { background-color: #990000; color: #00ff00; }
    p, span, label { color: #00ff00 !important; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("💀 YT-AUDIO COMMANDER")
st.write("---")

# קלט מהמשתמש
url = st.text_input("ENTER TARGET URL:", placeholder="https://youtube.com/...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("SELECT MISSION:", ["Download Only", "Download & Transcribe"])
with col2:
    quality = st.select_slider("AUDIO BITRATE:", options=["128", "192", "320"], value="192")

if url:
    if st.button("EXECUTE MISSION"):
        try:
            with st.status("🛠️ BREACHING YOUTUBE SERVERS...", expanded=True) as status:
                st.write("Extracting audio stream...")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality,
                    }],
                    'outtmpl': 'mission_audio.%(ext)s',
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio_file')
                
                st.write("Extraction complete. File encrypted.")
                
                if action == "Download & Transcribe":
                    st.write("Initiating transcription protocol...")
                    # כאן נשלב את Groq בהמשך
                    st.info("Transcription logic standing by for API Key.")
                
                status.update(label="MISSION ACCOMPLISHED", state="complete")

            with open("mission_audio.mp3", "rb") as f:
                st.audio(f.read())
                st.download_button(label="📥 DOWNLOAD SECURE MP3", data=f, file_name=f"{title}.mp3")
            
            os.remove("mission_audio.mp3")
            
        except Exception as e:
            st.error(f"SYSTEM FAILURE: {str(e)}")

st.write("---")
st.caption("STATUS: ENCRYPTED | OPERATOR: BOSS")
