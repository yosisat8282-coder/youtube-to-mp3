import streamlit as st
import yt_dlp
import os

# הגדרות דף
st.set_page_config(page_title="Audio-Tech Pro", page_icon="🎙️", layout="centered")

# עיצוב מותאם אישית - Cyber Modern
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    h1 {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
        font-weight: 800;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9, #2563eb);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }
    .stTextInput input {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px;
    }
    /* התאמה לעברית */
    div[data-testid="stMarkdownContainer"] p {
        text-align: right;
        direction: rtl;
    }
    label {
        text-align: right !important;
        display: block;
        direction: rtl;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Pro")
st.write("מערכת חכמה להורדת שמע ותמלול")
st.write("---")

# קלט מהמשתמש (מימין לשמאל)
url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://youtube.com/...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("בחר פעולה:", ["הורדה בלבד", "הורדה + תמלול"])
with col2:
    quality = st.select_slider("איכות שמע (kbps):", options=["128", "192", "320"], value="192")

if url:
    if st.button("הפעל פקודה"):
        try:
            with st.status("🚀 מעבד נתונים...", expanded=True) as status:
                st.write("שואב אודיו מיוטיוב...")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality,
                    }],
                    'outtmpl': 'output_audio.%(ext)s',
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio_file')
                
                if action == "הורדה + תמלול":
                    st.write("מתחיל תהליך תמלול חכם (Groq AI)...")
                    # כאן נכניס את פונקציית התמלול ברגע שיהיה לך API Key
                
                status.update(label="העיבוד הושלם בהצלחה!", state="complete")

            # הצגת הנגן וכפתור ההורדה
            with open("output_audio.mp3", "rb") as f:
                st.audio(f.read())
                st.download_button(label="📥 הורד קובץ MP3", data=f, file_name=f"{title}.mp3")
            
            os.remove("output_audio.mp3")
            
        except Exception as e:
            st.error(f"שגיאה במערכת: {str(e)}")

st.write("---")
st.caption("פיתוח: בוס | סטטוס מערכת: אונליין")
