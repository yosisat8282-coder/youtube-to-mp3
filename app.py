import streamlit as st
import requests
import base64

# הגדרות דף
st.set_page_config(page_title="Audio-Tech Ultra", page_icon="🎙️", layout="centered")

# עיצוב מודרני ויוקרתי (Dark Mode Pro)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f1f5f9; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border-radius: 12px; border: none; padding: 12px; font-weight: bold; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; text-align: center; }
    .status-card { background: rgba(30, 41, 59, 0.7); padding: 20px; border-radius: 15px; border: 1px solid #38bdf8; text-align: center; margin-top: 20px; direction: rtl; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Ultra")
st.write("מערכת מקצועית לחילוץ שיעורים והרצאות")
st.write("---")

# שדה API Key ל-Groq (מוחבא בהתחלה)
with st.expander("🔑 הגדרות תמלול AI (Groq)", expanded=False):
    groq_key = st.text_input("הכנס מפתח API לתמלול:", type="password")

url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    action = st.radio("בחר פעולה:", ["הורדה בלבד", "תמלול בלבד", "הורדה + תמלול"])
with col2:
    quality = st.select_slider("איכות שמע:", options=["64", "128", "192"], value="128")

if url:
    if st.button("בצע חילוץ מקצועי"):
        try:
            with st.status("🚀 מתחבר לשרתי המדיה... נא להמתין", expanded=True) as status:
                # שימוש ב-Piped API כדי לחסוך את החסימות של יוטיוב
                video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1]
                api_url = f"https://pipedapi.kavin.rocks/streams/{video_id}"
                
                response = requests.get(api_url, timeout=20)
                data = response.json()
                
                # מציאת קובץ השמע הטוב ביותר
                audio_streams = [s for s in data.get("audioStreams", []) if s.get("format") == "M4A"]
                if not audio_streams: audio_streams = data.get("audioStreams", [])
                
                audio_url = audio_streams[0].get("url")
                title = data.get("title", "Audio_Lesson")
                
                status.update(label="הקובץ מוכן!", state="complete")

            # הצגת התוצאה בתוך האתר שלך
            st.markdown(f"""
                <div class="status-card">
                    <h3 style="color:#38bdf8;">{title}</h3>
                    <p>הקובץ חולץ בהצלחה וממתין להורדה</p>
                    <hr style="border-color:#334155">
                    <audio controls style="width: 100%; margin-top: 10px;">
                        <source src="{audio_url}" type="audio/mp4">
                    </audio>
                </div>
            """, unsafe_allow_html=True)

            # כפתור הורדה אמיתי בתוך Streamlit (בלי לצאת מהאתר)
            audio_data = requests.get(audio_url).content
            st.download_button(
                label=f"📥 הורד את השיעור ({len(audio_data)//(1024*1024)} MB)",
                data=audio_data,
                file_name=f"{title}.mp3",
                mime="audio/mpeg"
            )

        except Exception as e:
            st.error(f"שגיאה בחילוץ: המערכת לא הצליחה לגשת לסרטון זה. וודא שהלינק תקין.")

st.write("---")
st.caption("פיתוח: בוס | טכנולוגיית Ultra-Stream 2026")
