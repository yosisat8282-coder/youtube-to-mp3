import streamlit as st
import yt_dlp
import os
import time

# הגדרות דף Pro
st.set_page_config(page_title="Audio-Tech Premium", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Modern יוקרתי ונקי (ללא גולגלות)
st.markdown("""
    <style>
    .stApp { background: #0b1120; color: #f8fafc; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border-radius: 12px; padding: 12px; font-weight: bold; width: 100%; border: none; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; text-align: center; }
    .status-card { background: #1e293b; padding: 20px; border-radius: 15px; border: 1px solid #38bdf8; text-align: center; margin-top: 20px; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; color: #94a3b8 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("Audio-Tech Premium")
st.write("מערכת מקצועית לחילוץ שיעורים והרצאות")
st.write("---")

# שדה API Key ל-Groq (כמו אצל שחר גולן)
with st.expander("🔑 הגדרות תמלול AI (Groq)", expanded=False):
    groq_key = st.text_input("הכנס מפתח API לתמלול:", type="password")

url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("בצע חילוץ שיעור"):
        try:
            with st.status("🚀 מתחבר ומחלץ נתונים... נא להמתין", expanded=True) as status:
                st.write("יוצר נתיב מאובטח ליוטיוב...")
                
                # הגדרות עקיפת חסימה (הסוואת דפדפן מלאה)
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '128',
                    }],
                    'outtmpl': 'lesson.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'referer': 'https://www.google.com/',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'Audio_Lesson')
                    file_path = "lesson.mp3"
                    file_size = os.path.getsize(file_path) / (1024 * 1024)
                
                status.update(label="החילוץ הושלם!", state="complete")

            # הצגת התוצאה
            st.markdown(f"""
                <div class="status-card">
                    <h3 style="color:#38bdf8;">{title}</h3>
                    <p style="color:#00ff00; font-weight:bold;">משקל הקובץ: {file_size:.2f} MB</p>
                    <hr style="border-color:#334155">
                </div>
            """, unsafe_allow_html=True)

            with open(file_path, "rb") as f:
                st.audio(f.read())
                st.download_button(
                    label=f"📥 הורד את השיעור ({file_size:.2f} MB)",
                    data=f,
                    file_name=f"{title}.mp3",
                    mime="audio/mpeg"
                )
            
            # ניקוי קובץ זמני
            os.remove(file_path)
            
        except Exception as e:
            st.error(f"שגיאת חילוץ: {str(e)}")
            st.info("טיפ: אם מופיעה שגיאת 403, נסה לעשות Reboot לאפליקציה ב-Streamlit Cloud.")

st.write("---")
st.caption("פיתוח: בוס | מצב: Pro System 2026")
