import streamlit as st
import yt_dlp
import os

# הגדרות דף
st.set_page_config(page_title="Audio-Tech Pro", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Tech משופר
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border-radius: 12px; width: 100%; font-weight: bold; }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; }
    .metric-box { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #38bdf8; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Pro")
st.write("מערכת חכמה לניהול תוכן אודיו")
st.write("---")

url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://youtube.com/...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("בחר משימה:", ["הורדה בלבד", "תמלול בלבד (ללא קובץ)", "הורדה + תמלול"])
with col2:
    quality = st.select_slider("בחר איכות (נמוך = חיסכון במקום):", 
                              options=["64", "128", "192", "320"], 
                              value="128",
                              help="64kbps חוסך המון מקום, 320kbps לאיכות שיא")

if url:
    if st.button("בצע משימה"):
        try:
            with st.status("🚀 מעבד נתונים...", expanded=True) as status:
                st.write("מתחבר לשרתי המדיה...")
                
                # הגדרות הורדה
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality,
                    }],
                    'outtmpl': 'temp_audio.%(ext)s',
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio_file')
                    file_path = "temp_audio.mp3"
                    
                    # חישוב גודל קובץ
                    file_size = os.path.getsize(file_path) / (1024 * 1024) # המרה ל-MB
                
                st.write(f"הקובץ מוכן. גודל מוערך: {file_size:.2f} MB")

                if "תמלול" in action:
                    st.write("מריץ פרוטוקול תמלול AI...")
                    # כאן יבוא הקוד של Groq ברגע שתזין API Key
                    st.info("התמלול יופיע כאן ברגע שנחבר את מפתח ה-API של Groq")

                status.update(label="המשימה הושלמה!", state="complete")

            # הצגת נתונים למשתמש
            st.markdown(f"""
                <div class="metric-box">
                    <h3 style="color:#38bdf8; margin:0;">פרטי הקובץ</h3>
                    <p style="margin:5px 0;">שם: {title}</p>
                    <p style="margin:5px 0; font-weight:bold; color:#00ff00;">משקל: {file_size:.2f} MB</p>
                </div>
            """, unsafe_allow_html=True)

            if "הורדה" in action:
                with open(file_path, "rb") as f:
                    st.audio(f.read())
                    st.download_button(label=f"📥 הורד קובץ ({file_size:.2f} MB)", 
                                     data=f, 
                                     file_name=f"{title}.mp3")
            
            # ניקוי קבצים זמניים
            if os.path.exists(file_path):
                os.remove(file_path)
            
        except Exception as e:
            st.error(f"שגיאה במערכת: {str(e)}")

st.write("---")
st.caption("פיתוח: בוס | מצב: Cyber-Modern Mode")
