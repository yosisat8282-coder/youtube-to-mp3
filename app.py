import streamlit as st
import yt_dlp
import os
from groq import Groq
import requests

# הגדרות דף Pro
st.set_page_config(page_title="Audio-Tech Ultra", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Tech יוקרתי (עברית RTL)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border-radius: 12px; padding: 12px; font-weight: bold; width: 100%; border: none; }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; text-align: right; }
    .status-card { background: rgba(30, 41, 59, 0.7); padding: 20px; border-radius: 15px; border: 1px solid #38bdf8; text-align: center; margin-top: 20px; }
    .transcription-box { background: #1e293b; padding: 15px; border-radius: 10px; border-right: 5px solid #38bdf8; direction: rtl; text-align: right; margin-top: 10px; white-space: pre-wrap; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; color: #94a3b8 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Ultra")
st.write("המערכת הסופית להורדה ותמלול שיעורים")
st.write("---")

# אזור הגדרות API
with st.expander("🔑 הגדרות מפתח API (Groq)", expanded=False):
    api_key_input = st.text_input("הכנס מפתח API של Groq:", type="password")

url = st.text_input("הדבק לינק מהיוטיוב כאן:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("בחר פעולה:", ["הורדה בלבד", "תמלול בלבד", "הורדה + תמלול"])
with col2:
    quality = st.select_slider("איכות שמע (kbps):", options=["64", "128", "192"], value="128")

if url:
    if st.button("🚀 הפעל מערכת"):
        if ("תמלול" in action) and not api_key_input:
            st.error("בוס, שכחת להזין מפתח API לתמלול!")
        else:
            try:
                with st.status("מעבד נתונים... נא להמתין", expanded=True) as status:
                    st.write("מתחבר ליוטיוב ומחלץ שמע...")
                    
                    output_file = "temp_audio.mp3"
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': quality,
                        }],
                        'outtmpl': 'temp_audio',
                        'quiet': True,
                        'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        title = info.get('title', 'שיעור ללא שם')
                    
                    file_size = os.path.getsize(output_file) / (1024 * 1024)
                    
                    transcription_text = ""
                    if "תמלול" in action:
                        st.write("מבצע תמלול AI בטכנולוגיית Whisper...")
                        client = Groq(api_key=api_key_input)
                        with open(output_file, "rb") as file:
                            transcription = client.audio.transcriptions.create(
                                file=(output_file, file.read()),
                                model="whisper-large-v3",
                                response_format="text",
                                language="he"
                            )
                            transcription_text = transcription
                    
                    status.update(label="המשימה הושלמה!", state="complete")

                # הצגת התוצאות
                st.markdown(f"""
                    <div class="status-card">
                        <h3 style="color:#38bdf8;">{title}</h3>
                        <p style="color:#00ff00;">משקל: {file_size:.2f} MB</p>
                    </div>
                """, unsafe_allow_html=True)

                if transcription_text:
                    st.subheader("📝 תמלול השיעור:")
                    st.markdown(f'<div class="transcription-box">{transcription_text}</div>', unsafe_allow_html=True)
                    st.download_button("📥 הורד תמלול (TXT)", transcription_text, file_name=f"{title}.txt")

                if "הורדה" in action:
                    with open(output_file, "rb") as f:
                        st.audio(f.read())
                        st.download_button(label=f"📥 הורד שיעור ({file_size:.2f} MB)", data=f, file_name=f"{title}.mp3")
                
                if os.path.exists(output_file):
                    os.remove(output_file)
                    
            except Exception as e:
                st.error(f"שגיאה: {str(e)}")
                st.info("אם מופיעה שגיאת 403, וודא שעשית Reboot לאפליקציה ב-Streamlit Cloud.")

st.write("---")
st.caption("פיתוח: בוס | טכנולוגיית Ultra-Stream 2026")
