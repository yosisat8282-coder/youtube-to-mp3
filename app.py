import streamlit as st
import yt_dlp
import os
from groq import Groq
import tempfile

# הגדרות דף Pro
st.set_page_config(page_title="Audio-Tech Ultra", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Tech RTL יוקרתי
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .stApp { background: #0b0f19; color: #e2e8f0; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    .stButton>button { background: linear-gradient(90deg, #3b82f6, #8b5cf6); color: white; border: none; border-radius: 12px; padding: 12px; font-weight: bold; width: 100%; transition: 0.3s; }
    .stTextInput input { background-color: #111827 !important; color: white !important; border: 1px solid #1f2937 !important; text-align: right; }
    .status-card { background: #1f2937; padding: 20px; border-radius: 15px; border: 1px solid #374151; margin-top: 20px; text-align: center; }
    .transcription-box { background: #111827; padding: 15px; border-radius: 12px; border-right: 5px solid #60a5fa; direction: rtl; text-align: right; color: #cbd5e1; white-space: pre-wrap; margin-top: 10px; line-height: 1.6; }
    label { text-align: right !important; display: block; direction: rtl; color: #94a3b8 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Ultra")
st.write("מערכת פרימיום לחילוץ ותמלול שיעורים (2026)")
st.write("---")

# בדיקת מפתחות ב-Secrets
has_cookies = "YT_COOKIES" in st.secrets
has_groq = "GROQ_API_KEY" in st.secrets

url = st.text_input("הדבק לינק מהיוטיוב:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("בחר פעולה:", ["הורדה בלבד", "תמלול בלבד", "הורדה + תמלול"])
with col2:
    quality = st.select_slider("איכות שמע (kbps):", options=["64", "128", "192"], value="128")

if url:
    if st.button("🚀 הפעל עיבוד שיעור"):
        try:
            with st.status("מעבד נתונים... נא להמתין", expanded=True) as status:
                
                cookie_path = None
                if has_cookies:
                    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt", encoding="utf-8") as tmp:
                        tmp.write(st.secrets["YT_COOKIES"])
                        cookie_path = tmp.name
                    st.write("✅ אימות Stealth הופעל.")

                # שימוש בפורמט ba (Best Audio) עם גיבוי ל-b (Best Video)
                # זה פותר את שגיאת ה-Requested format is not available
                output_filename = "final_audio"
                ydl_opts = {
                    'format': 'bestaudio/best', 
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality,
                    }],
                    'outtmpl': output_filename,
                    'cookiefile': cookie_path,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'nocheckcertificate': True,
                    'quiet': True,
                    'no_warnings': True,
                }

                st.write("שואב נתוני שמע מהשרת...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get('title', 'שיעור')
                
                transcription_text = ""
                actual_file = "final_audio.mp3"

                if "תמלול" in action:
                    if has_groq:
                        st.write("מפענח שמע לטקסט (Groq AI)...")
                        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        with open(actual_file, "rb") as audio_file:
                            transcription_text = client.audio.trans
