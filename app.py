import streamlit as st
import requests
import time

# הגדרות דף Pro
st.set_page_config(page_title="Audio-Tech Premium", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Modern יוקרתי (נקי, מקצועי, ללא גולגלות)
st.markdown("""
    <style>
    .stApp { background: #0b1120; color: #f8fafc; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border: none; border-radius: 12px; padding: 12px; font-weight: bold; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; text-align: center; }
    .download-card { background: #1e293b; padding: 25px; border-radius: 15px; border: 1px solid #38bdf8; text-align: center; margin-top: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; font-weight: bold; color: #94a3b8 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("Audio-Tech Premium")
st.write("מערכת מקצועית להורדה ותמלול שיעורים")
st.write("---")

# שדה API Key ל-Groq (כמו אצל שחר גולן)
with st.expander("🔑 הגדרות תמלול AI (Groq)", expanded=False):
    groq_key = st.text_input("הכנס מפתח API לתמלול:", type="password")

url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("בצע חילוץ שיעור"):
        try:
            with st.status("🚀 מתחבר לשרת המדיה... נא להמתין", expanded=True) as status:
                # שימוש בשרת API יציב שמחזיר לינקים ישירים
                video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1]
                
                # שליחת בקשה למנוע הורדה חזק
                api_url = f"https://api.cobalt.tools/api/json"
                payload = {"url": url, "downloadMode": "audio", "audioFormat": "mp3"}
                headers = {"Accept": "application/json", "Content-Type": "application/json"}
                
                response = requests.post(api_url, json=payload, headers=headers)
                data = response.json()
                
                if data.get("status") in ["stream", "redirect"]:
                    download_url = data.get("url")
                    st.write("השיעור אותר. מכין נגן שמע...")
                    
                    status.update(label="החילוץ הושלם בהצלחה!", state="complete")
                    
                    # הצגת התוצאה בתוך ה-Card המעוצב
                    st.markdown(f"""
                        <div class="download-card">
                            <h3 style="color:#38bdf8; margin-bottom:15px;">🎧 השיעור מוכן לשמיעה והורדה</h3>
                            <audio controls style="width: 100%; border-radius: 8px;">
                                <source src="{download_url}" type="audio/mpeg">
                            </audio>
                            <br><br>
                            <a href="{download_url}" target="_blank" style="text-decoration:none;">
                                <div style="background: #10b981; color: white; padding: 15px; border-radius: 10px; font-weight: bold; cursor: pointer;">
                                    📥 לחץ כאן להורדת הקובץ למחשב
                                </div>
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("השרת עמוס מדי כרגע. נסה שוב בעוד דקה.")
                    
        except Exception as e:
            st.error("שגיאת תקשורת. וודא שהלינק תקין ונסה שוב.")

st.write("---")
st.caption("פיתוח: בוס | טכנולוגיית Ultra-Stream 2026")
