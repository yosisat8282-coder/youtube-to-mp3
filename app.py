import streamlit as st
import yt_dlp
import os
from groq import Groq
import tempfile

# הגדרות דף Pro
st.set_page_config(page_title="Audio-Tech Ultra", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Tech יוקרתי (עברית RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stApp { background: #0b0f19; color: #e2e8f0; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; font-size: 3rem !important; }
    .stButton>button { background: linear-gradient(90deg, #3b82f6, #8b5cf6); color: white; border: none; border-radius: 12px; padding: 12px; font-weight: bold; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(139, 92, 246, 0.4); }
    .stTextInput input { background-color: #111827 !important; color: #f8fafc !important; border: 1px solid #1f2937 !important; border-radius: 10px; text-align: right; }
    .status-card { background: #1f2937; padding: 25px; border-radius: 15px; border: 1px solid #374151; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .transcription-box { background: #111827; padding: 20px; border-radius: 12px; border-right: 5px solid #60a5fa; direction: rtl; text-align: right; margin-top: 15px; color: #cbd5e1; white-space: pre-wrap; line-height: 1.6; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; color: #94a3b8 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Ultra")
st.write("מערכת פרימיום לחילוץ ותמלול שיעורים והרצאות")
st.write("---")

# בדיקת הגדרות ב-Secrets
has_cookies = "YT_COOKIES" in st.secrets
has_groq = "GROQ_API_KEY" in st.secrets

url = st.text_input("הדבק לינק מהיוטיוב:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("בחר פעולה:", ["הורדה בלבד", "תמלול בלבד", "הורדה + תמלול"])
with col2:
    quality = st.select_slider("איכות שמע (kbps):", options=["64", "128", "192"], value="128")

if url:
    if st.button("🚀 התחל בעיבוד השיעור"):
        try:
            with st.status("מתחבר ומעבד... נא להמתין", expanded=True) as status:
                
                # טיפול בעוגיות
                cookie_path = None
                if has_cookies:
                    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as temp_cookie:
                        temp_cookie.write(st.secrets["YT_COOKIES"])
                        cookie_path = temp_cookie.name
                    st.write("✅ אימות משתמש הופעל בהצלחה.")
                
                output_file = "lesson_audio.mp3"
                
                # הגדרות הורדה גמישות וחסינות
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality,
                    }],
                    'outtmpl': 'lesson_audio',
                    'cookiefile': cookie_path,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True
                }

                st.write("שואב נתוני שמע מיוטיוב...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'שיעור ללא שם')
                
                transcription_text = ""
                if "תמלול" in action:
                    if has_groq:
                        st.write("מבצע תמלול AI (Whisper-large-v3)...")
                        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        with open("lesson_audio.mp3", "rb") as audio_file:
                            transcription = client.audio.transcriptions.create(
                                file=("lesson_audio.mp3", audio_file.read()),
                                model="whisper-large-v3",
                                language="he",
                                response_format="text"
                            )
                            transcription_text = transcription
                    else:
                        st.error("מפתח Groq חסר ב-Secrets!")

                status.update(label="המשימה הושלמה!", state="complete")

            # תצוגת התוצאה הסופית
            st.markdown(f'<div class="status-card"><h3>✅ {title}</h3></div>', unsafe_allow_html=True)

            if transcription_text:
                st.subheader("📝 תמלול השיעור:")
                st.markdown(f'<div class="transcription-box">{transcription_text}</div>', unsafe_allow_html=True)
                st.download_button("📥 הורד תמלול כקובץ טקסט", transcription_text, file_name=f"{title}.txt")

            if "הורדה" in action:
                with open("lesson_audio.mp3", "rb") as f:
                    st.audio(f.read())
                    st.download_button(label="📥 הורד קובץ שמע (MP3)", data=f, file_name=f"{title}.mp3")

            # ניקוי קבצים זמניים
            if os.path.exists("lesson_audio.mp3"): os.remove("lesson_audio.mp3")
            if cookie_path and os.path.exists(cookie_path): os.remove(cookie_path)
                
        except Exception as e:
            st.error(f"שגיאה במערכת: {str(e)}")
            st.info("בוס, אם השגיאה נמשכת, וודא שהעוגיות ב-Secrets מעודכנות.")

st.write("---")
st.caption("Operator: Boss | Version: 2026.4.0")
