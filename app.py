import streamlit as st
import yt_dlp
import os

# הגדרות דף
st.set_page_config(page_title="Audio-Tech Pro", page_icon="📚", layout="centered")

# עיצוב Cyber-Tech
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border-radius: 12px; width: 100%; font-weight: bold; border: none; padding: 10px; }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 מוריד שיעורים והרצאות")
st.write("אופטימיזציה לסרטונים ארוכים")
st.write("---")

url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://youtube.com/watch?v=...")

quality = st.select_slider("איכות שמע (64 מומלץ לשיעורים ארוכים מאוד):", 
                          options=["64", "128", "192"], 
                          value="128")

if url:
    if st.button("התחל הורדת שיעור"):
        try:
            with st.status("🚀 מעבד את השיעור... נא להמתין", expanded=True) as status:
                st.write("מתחבר ליוטיוב באמצעות מעקף...")
                
                # הגדרות קשוחות לעקיפת חסימות וטיפול בקבצים ארוכים
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality,
                    }],
                    'outtmpl': 'lesson_audio.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'source_address': '0.0.0.0', # עוזר לעקוף חסימות IP
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio_file')
                    file_path = "lesson_audio.mp3"
                    file_size = os.path.getsize(file_path) / (1024 * 1024)
                
                status.update(label="השיעור מוכן!", state="complete")

            st.success(f"סיום עיבוד: {title}")
            st.info(f"משקל הקובץ: {file_size:.2f} MB")

            with open(file_path, "rb") as f:
                st.audio(f.read())
                st.download_button(label=f"📥 הורד שיעור ({file_size:.2f} MB)", 
                                 data=f, 
                                 file_name=f"{title}.mp3")
            
            # ניקוי קובץ זמני מהשרת
            if os.path.exists(file_path):
                os.remove(file_path)
            
        except Exception as e:
            st.error(f"שגיאה: יוטיוב חסם את הבקשה. נסה שוב בעוד דקה או השתמש בלינק אחר.")

st.write("---")
st.caption("פיתוח: בוס | מותאם להרצאות ארוכות")
