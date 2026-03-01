import streamlit as st
import yt_dlp
import os
from groq import Groq

# הגדרות דף פרימיום
st.set_page_config(page_title="Audio-Tech Ultra", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Tech (נקי, מקצועי, ללא גולגלות)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f1f5f9; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border-radius: 12px; padding: 12px; font-weight: bold; width: 100%; border: none; }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; text-align: right; }
    .status-card { background: rgba(30, 41, 59, 0.7); padding: 20px; border-radius: 15px; border: 1px solid #38bdf8; text-align: center; margin-top: 20px; }
    .transcription-box { background: #1e293b; padding: 15px; border-radius: 10px; border-right: 5px solid #38bdf8; direction: rtl; text-align: right; margin-top: 10px; white-space: pre-wrap; color: #e2e8f0; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; color: #94a3b8 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Ultra")
st.write("מערכת פרימיום להורדה ותמלול שיעורים (Stealth Mode)")
st.write("---")

# בדיקת תקינות הגדרות
has_cookies = "YT_COOKIES" in st.secrets
has_groq = "GROQ_API_KEY" in st.secrets

if not has_cookies:
    st.warning("⚠️ שים לב: לא זוהו עוגיות ב-Secrets. ייתכן שתתקבל שגיאת 403.")

url = st.text_input("הדבק לינק לשיעור כאן:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("בחר משימה:", ["הורדה בלבד", "תמלול בלבד", "הורדה + תמלול"])
with col2:
    quality = st.select_slider("איכות שמע (kbps):", options=["64", "128", "192"], value="128")

if url:
    if st.button("🚀 הפעל מערכת"):
        try:
            with st.status("מעבד נתונים... נא להמתין", expanded=True) as status:
                # יצירת קובץ עוגיות זמני
                cookie_path = "cookies.txt"
                if has_cookies:
                    with open(cookie_path, "w", encoding="utf-8") as f:
                        f.write(st.secrets["YT_COOKIES"])
                    st.write("✅ עוגיות זוהו והופעלו.")

                output_file = "lesson_audio.mp3"
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': quality}],
                    'outtmpl': 'lesson_audio',
                    'cookiefile': cookie_path if has_cookies else None,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'quiet': True,
                    'no_warnings': True
                }

                st.write("מוריד שמע מיוטיוב...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'שיעור')
                
                transcription_text = ""
                if "תמלול" in action:
                    if has_groq:
                        st.write("מבצע תמלול AI מהיר (Groq)...")
                        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        with open(output_file, "rb") as f:
                            transcription_text = client.audio.transcriptions.create(
                                file=(output_file, f.read()),
                                model="whisper-large-v3",
                                language="he",
                                response_format="text"
                            )
                    else:
                        st.error("מפתח Groq חסר ב-Secrets!")

                status.update(label="המשימה הושלמה!", state="complete")

            # תצוגת התוצאות
            st.markdown(f'<div class="status-card"><h3 style="color:#38bdf8;">{title}</h3></div>', unsafe_allow_html=True)

            if transcription_text:
                st.subheader("📝 תמלול השיעור:")
                st.markdown(f'<div class="transcription-box">{transcription_text}</div>', unsafe_allow_html=True)
                st.download_button("📥 הורד תמלול (TXT)", transcription_text, file_name=f"{title}.txt")

            if "הורדה" in action:
                with open(output_file, "rb") as f:
                    st.audio(f.read())
                    st.download_button(label="📥 הורד שיעור (MP3)", data=f, file_name=f"{title}.mp3")

            # ניקוי
            if os.path.exists(output_file): os.remove(output_file)
            if os.path.exists(cookie_path): os.remove(cookie_path)

        except Exception as e:
            st.error(f"שגיאה במערכת: {str(e)}")
