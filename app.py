import streamlit as st
import yt_dlp
import os

# הגדרות דף
st.set_page_config(page_title="Audio-Tech Pro", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Tech יוקרתי בעברית
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border-radius: 12px; width: 100%; font-weight: bold; border: none; padding: 10px; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(37,99,235,0.4); }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; }
    .metric-box { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #38bdf8; margin: 10px 0; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; font-weight: bold; }
    .stRadio div[role="radiogroup"] { direction: rtl; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Pro")
st.write("מערכת חכמה להורדת שמע וניתוח תוכן")
st.write("---")

# קלט מהמשתמש
url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://youtube.com/...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("בחר משימה:", ["הורדה בלבד", "תמלול בלבד (בקרוב)", "הורדה + תמלול"])
with col2:
    quality = st.select_slider("איכות שמע (נמוך חוסך מקום):", 
                              options=["64", "128", "192", "320"], 
                              value="128")

if url:
    if st.button("בצע משימה"):
        try:
            with st.status("🚀 מעבד נתונים... נא להמתין", expanded=True) as status:
                st.write("מתחבר לשרת ויוצר הסוואה...")
                
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality,
                    }],
                    'outtmpl': 'temp_audio.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio_file')
                    file_path = "temp_audio.mp3"
                    
                    # חישוב משקל קובץ
                    file_size = os.path.getsize(file_path) / (1024 * 1024)
                
                st.write(f"הקובץ מוכן לעבודה.")
                status.update(label="המשימה הושלמה!", state="complete")

            # הצגת תיבת נתונים מעוצבת
            st.markdown(f"""
                <div class="metric-box">
                    <h3 style="color:#38bdf8; margin:0;">פרטי הקובץ</h3>
                    <p style="margin:5px 0; font-size: 1.1em;">{title}</p>
                    <p style="margin:5px 0; font-weight:bold; color:#00ff00; font-size: 1.2em;">משקל: {file_size:.2f} MB</p>
                </div>
            """, unsafe_allow_html=True)

            if "הורדה" in action:
                with open(file_path, "rb") as f:
                    st.audio(f.read())
                    st.download_button(label=f"📥 הורד קובץ ({file_size:.2f} MB)", 
                                     data=f, 
                                     file_name=f"{title}.mp3")
            
            # ניקוי קבצים
            if os.path.exists(file_path):
                os.remove(file_path)
            
        except Exception as e:
            st.error(f"שגיאה במערכת: {str(e)}")

st.write("---")
st.caption("פיתוח: בוס | Cyber-Tech Mode 2026")
