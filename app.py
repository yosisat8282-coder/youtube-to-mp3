import streamlit as st
import requests

st.set_page_config(page_title="Audio-Tech Pro | שיעורים והרצאות", page_icon="📚", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border-radius: 10px; height: 3em; font-weight: bold; width: 100%; }
    .stTextInput input { background-color: #1e293b !important; color: white !important; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; }
    .info-box { background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; padding: 15px; border-radius: 10px; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 מוריד שיעורים והרצאות")
st.write("מערכת ייעודית לקבצים ארוכים וכבדים")

st.markdown("""
<div class="info-box">
💡 <b>טיפ לבוס:</b> עבור שיעורים ארוכים, המערכת תייצר לינק ישיר. 
אם הסרטון מעל שעה, מומלץ להשתמש באיכות 64kbps או 128kbps כדי לחסוך מקום בטלפון.
</div>
""", unsafe_allow_html=True)

st.write("---")

url = st.text_input("הדבק לינק לשיעור מיוטיוב:", placeholder="https://youtube.com/watch?v=...")

quality = st.select_slider("איכות שמע (נמוך מומלץ לשיעורים ארוכים):", 
                          options=["64", "128", "192", "320"], 
                          value="128")

if url:
    if st.button("חלץ שיעור להורדה"):
        try:
            with st.spinner("מתחבר לשרתי המדיה... זה עשוי לקחת כמה שניות לסרטון ארוך"):
                # שימוש בשרת Cobalt יציב
                payload = {
                    "url": url,
                    "downloadMode": "audio",
                    "audioFormat": "mp3",
                    "audioBitrate": quality,
                    "isNoTTWatermark": True
                }
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
                
                # פנייה לשרת חזק יותר
                response = requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers)
                data = response.json()
                
                if data.get("status") == "stream" or data.get("status") == "picker" or data.get("status") == "redirect":
                    download_url = data.get("url")
                    st.success("✅ השיעור מוכן להורדה!")
                    
                    st.markdown(f"""
                        <div style="text-align: center; margin-top: 20px;">
                            <a href="{download_url}" target="_blank" style="text-decoration: none;">
                                <button style="background-color: #10b981; color: white; padding: 15px 30px; border: none; border-radius: 10px; font-size: 1.2em; cursor: pointer; font-weight: bold;">
                                     לחץ כאן להורדת השיעור (MP3) 📥
                                </button>
                            </a>
                            <p style="margin-top:10px; font-size: 0.9em; color: #94a3b8;">הלינק יפתח את הקובץ להורדה ישירה</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.audio(download_url)
                else:
                    st.error("לא הצלחתי למצוא את הסרטון. וודא שהלינק תקין (לא Playlist).")
                    
        except Exception as e:
            st.error(f"שגיאה בתקשורת: {e}")

st.write("---")
st.caption("סטטוס מערכת: אופטימיזציה לשיעורים ארוכים | 2026")
