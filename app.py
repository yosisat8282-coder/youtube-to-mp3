import streamlit as st
import requests

# הגדרות דף
st.set_page_config(page_title="Audio-Tech Pro | שיעורים", page_icon="📚", layout="centered")

# עיצוב Cyber-Tech נקי וקבוע
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    .main-btn { 
        background: linear-gradient(90deg, #0ea5e9, #2563eb); 
        color: white !important; 
        border-radius: 12px; 
        width: 100%; 
        padding: 15px; 
        text-align: center; 
        display: block; 
        font-weight: bold; 
        text-decoration: none;
        margin-top: 10px;
        border: none;
    }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ מוריד שיעורים Audio-Tech")
st.write("גרסה יציבה לעקיפת חסימות יוטיוב")
st.write("---")

# קלט מהמשתמש
url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://youtube.com/watch?v=...")

# כפתור ההורדה הקבוע
if st.button("בצע הורדה / חילוץ"):
    if url:
        try:
            with st.spinner("מייצר לינק הורדה מאובטח..."):
                # שימוש בשרת חיצוני (Cobalt) כדי למנוע חסימת 403 מהשרת שלך
                payload = {
                    "url": url,
                    "downloadMode": "audio",
                    "audioFormat": "mp3",
                    "audioBitrate": "128"
                }
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
                
                # פנייה לשרת חזק שעוקף את החסימות
                response = requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers)
                data = response.json()
                
                if data.get("status") == "stream" or data.get("status") == "picker" or data.get("status") == "redirect":
                    download_url = data.get("url")
                    
                    st.success("✅ השיעור מוכן!")
                    
                    # הצגת נגן השמע (אם הקובץ לא גדול מדי לתצוגה)
                    st.audio(download_url)
                    
                    # כפתור ההורדה הישיר שתמיד יעבוד
                    st.markdown(f"""
                        <a href="{download_url}" target="_blank" class="main-btn">
                             📥 לחץ כאן להורדת הקובץ למכשיר
                        </a>
                    """, unsafe_allow_html=True)
                    st.info("ההורדה תתבצע ישירות מהדפדפן שלך כדי למנוע חסימות שרת.")
                else:
                    st.error("לא הצלחתי לחלץ את הסרטון. ייתכן שהסרטון מוגן או שהלינק לא תקין.")
        except Exception as e:
            st.error(f"שגיאה בתקשורת: {str(e)}")
    else:
        st.warning("אנא הדבק לינק לפני הלחיצה.")

st.write("---")
st.caption("פיתוח: בוס | סטטוס: Active Stealth Mode")
