import streamlit as st
import yt_dlp
import os

# הגדרות דף Pro
st.set_page_config(page_title="Audio-Tech Premium", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Tech יוקרתי (נקי, מקצועי, ללא גולגלות)
st.markdown("""
    <style>
    .stApp { background: #0b1120; color: #f8fafc; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border: none; border-radius: 12px; padding: 12px; font-weight: bold; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; text-align: center; }
    .result-card { background: #1e293b; padding: 25px; border-radius: 15px; border: 1px solid #38bdf8; text-align: center; margin-top: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; font-weight: bold; color: #94a3b8 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("Audio-Tech Premium")
st.write("מערכת מקצועית להורדת שיעורים והרצאות")
st.write("---")

url = st.text_input("הדבק לינק מהיוטיוב:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("🚀 התחל חילוץ שיעור"):
        try:
            with st.status("מנתח את השיעור... נא להמתין", expanded=True) as status:
                st.write("מתחבר ליוטיוב דרך נתיב מאובטח...")
                
                # הגדרות חזקות לעקיפת חסימות 403
                save_path = "lesson.mp3"
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '128',
                    }],
                    'outtmpl': 'lesson',
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'שיעור ללא שם')
                    file_name = f"{title}.mp3"
