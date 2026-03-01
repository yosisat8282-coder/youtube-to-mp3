import streamlit as st
import yt_dlp
import os
from groq import Groq

# הגדרות דף ועיצוב Cyber-Tech
st.set_page_config(page_title="Audio-Tech Pro", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border-radius: 12px; width: 100%; font-weight: bold; border: none; padding: 10px; }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; }
    .metric-box { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #38bdf8; margin: 10px 0; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; }
    .transcription-box { background: #1e293b; padding: 15px; border-radius: 10px; border-left: 5px solid #38bdf8; direction: rtl; text-align: right; color: #f1f5f9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Pro")
st.write("מערכת חכמה להורדה ותמלול AI")
st.write("---")

# --- אזור הגדרת API KEY ---
with st.expander("🔑 הגדרות מפתח API (Groq)", expanded=False):
    api_key_input = st.text_input("הכנס את מפתח ה-API שלך מ-Groq:", type="password")

# --- קלט משתמש ---
url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://youtube.com/...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("בחר משימה:", ["הורדה בלבד", "תמלול בלבד", "הורדה + תמלול"])
with col2:
    quality = st.select_slider("איכות שמע (kbps):", options=["64", "128", "192", "320"], value="128")

if url:
    if st.button("בצע משימה"):
        if ("תמלול" in action) and not api_key_input:
            st.error("חובה להזין מפתח API לתמלול!")
        else:
            try:
                with st.status("🚀 מבצע מעקף וחילוץ נתונים...", expanded=True) as status:
                    
                    # הבלוק המנצח ל-403
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': quality,
                        }],
                        'outtmpl': 'final_audio.%(ext)s',
                        'quiet': True,
                        'no_warnings': True,
                        'nocheckcertificate': True,
                        'ignoreerrors': False,
                        'logtostderr': False,
                        'add_header': [
                            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                            'Accept-Language: en-US,en;q=0.5',
                            'Sec-Fetch-Mode: navigate'
                        ]
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        st.write("מתחבר לשרת...")
                        info = ydl.extract_info(url, download=True)
                        title = info.get('title', 'audio_file')
                        file_path = "final_audio.mp3"
                        file_size = os.path.getsize(file_path) / (1024 * 1024)

                    transcription_text = ""
                    if "תמלול" in action:
                        st.write("שולח לתמלול ב-Groq Cloud...")
                        client = Groq(api_key=api_key_input)
                        with open(file_path, "rb") as file:
                            transcription = client.audio.transcriptions.create(
                                file=(file_path, file.read()),
                                model="whisper-large-v3",
                                response_format="text",
                                language="he"
                            )
                            transcription_text = transcription
                    
                    status.update(label="המשימה הושלמה!", state="complete")

                st.markdown(f"""<div class="metric-box"><h3 style="color:#38bdf8; margin:0;">{title}</h3><p style="color:#00ff00;">משקל: {file_size:.2f} MB</p></div>""", unsafe_allow_html=True)

                if transcription_text:
                    st.subheader("📝 תמלול:")
                    st.markdown(f'<div class="transcription-box">{transcription_text}</div>', unsafe_allow_html=True)

                if "הורדה" in action:
                    with open(file_path, "rb") as f:
                        st.audio(f.read())
                        st.download_button(label=f"📥 הורד קובץ ({file_size:.2f} MB)", data=f, file_name=f"{title}.mp3")
                
                if os.path.exists(file_path):
                    os.remove(file_path)
                
            except Exception as e:
                st.error(f"שגיאה: {str(e)}")

st.write("---")
st.caption("פיתוח: בוס | מצב: Stealth Mode 2026")
