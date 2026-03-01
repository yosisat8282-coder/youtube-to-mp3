import streamlit as st
import requests
import re

# הגדרות דף
st.set_page_config(page_title="Audio-Tech Ultra", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Tech משופר
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    h1 { color: #38bdf8; text-align: center; font-weight: 800; }
    .stButton>button { 
        background: #2563eb; color: white; border-radius: 8px; 
        width: 100%; font-weight: bold; border: none; padding: 12px;
    }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; }
    .download-card {
        background: rgba(56, 189, 248, 0.1);
        border: 2px solid #38bdf8;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Ultra")
st.write("מערכת חילוץ שיעורים - מעקף חסימות מתקדם")
st.write("---")

# פונקציה לניקוי הלינק
def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

url_input = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://www.youtube.com/watch?v=...")

if url_input:
    video_id = get_video_id(url_input)
    if video_id:
        if st.button("🚀 חלץ שיעור להורדה"):
            try:
                with st.spinner("מבצע מעקף חסימות..."):
                    # שימוש בשרת API חזק ואמין יותר (Invidious/Piped API)
                    api_url = f"https://pipedapi.kavin.rocks/streams/{video_id}"
                    response = requests.get(api_url, timeout=15)
                    data = response.json()
                    
                    # חיפוש האודיו הכי טוב ברשימה
                    audio_streams = [s for s in data.get("audioStreams", []) if s.get("format") == "M4A" or s.get("format") == "WEB_M"]
                    
                    if audio_streams:
                        # לוקחים את הסטרים הראשון (בדרך כלל האיכותי והיציב ביותר)
                        final_link = audio_streams[0].get("url")
                        title = data.get("title", "Lesson_Audio")
                        
                        st.markdown(f"""
                            <div class="download-card">
                                <h3 style="color:#38bdf8;">✅ השיעור חולץ בהצלחה!</h3>
                                <p><b>שם השיעור:</b> {title}</p>
                                <hr style="border-color:#334155;">
                                <audio controls style="width:100%; margin-bottom:15px;">
                                    <source src="{final_link}" type="audio/mp4">
                                </audio>
                                <a href="{final_link}" target="_blank" style="text-decoration:none;">
                                    <button style="background:#10b981; color:white; padding:15px; border:none; border-radius:8px; width:100%; font-weight:bold; cursor:pointer;">
                                        📥 הורד קובץ שמע למכשיר
                                    </button>
                                </a>
                                <p style="font-size:0.8em; color:#94a3b8; margin-top:10px;">ההורדה תתבצע ישירות מהשרת כדי למנוע חסימה</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("לא נמצאו נתיבי שמע לסרטון זה. נסה סרטון אחר.")
            except Exception as e:
                st.error("המערכת עמוסה כרגע. נסה שוב בעוד כמה דקות.")
    else:
        st.warning("הלינק שהזנת לא נראה כמו לינק תקין של יוטיוב.")

st.write("---")
st.caption("מצב: Ultra Stealth | 2026")
