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
                
              # הגדרות הורדה עם מעקף חסימה (הבלוק החדש)
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
                    'referer': 'https://www.google.com/',
                }
