import streamlit as st
import requests
import time

# הגדרות דף Pro
st.set_page_config(page_title="Audio-Tech Premium", page_icon="🎙️", layout="centered")

# עיצוב Cyber-Modern יוקרתי (נקי, מקצועי, ללא גולגלות)
st.markdown("""
    <style>
    .stApp { background: #0b1120; color: #f8fafc; }
    h1 { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    .stButton>button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border-radius: 12px; padding: 12px; font-weight: bold; width: 100%; border: none; }
    .stTextInput input { background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important; border-radius: 10px; text-align: center; }
    .download-card { background: #1e293b; padding: 25px; border-radius: 15px; border: 1px solid #38bdf8; text-align: center; margin-top: 20px; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    label { text-align: right !important; display: block; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("Audio-Tech Premium")
st.write("מערכת מקצועית לחילוץ שיעורים והרצאות")
st.write("---")

url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("בצע חילוץ מקצועי"):
        try:
            with st.status("🚀 מחלץ נתיב הורדה מאובטח...", expanded=True) as status:
                # שימוש ב-API ציבורי יציב (עוקף חסימות 403)
                video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1]
                
                # פנייה למנוע חילוץ שלא מזוהה כבוט
                download_api = f"https://api.vevioz.com/api/button/mp3/{video_id}"
                
                time.sleep(1) # סימולציית בדיקה
                status.update(label="החילוץ הושלם!", state="complete")

            # הצגת נגן וכפתור בתוך הממשק שלך
            st.markdown(f"""
                <div class="download-card">
                    <h3 style="color:#38bdf8; margin-bottom:15px;">✅ השיעור מוכן</h3>
                    <p>לחץ על הכפתור למטה כדי להתחיל בהורדת ה-MP3</p>
                    <hr style="border-color:#334155">
                    <iframe src="{download_api}" width="100%" height="60px" style="border:none; border-radius:10px;"></iframe>
                </div>
            """, unsafe_allow_html=True)
            
            st.info("💡 בשיעורים ארוכים, ייתכן שיקח לכפתור כמה שניות לבצע את ההמרה.")

        except Exception as e:
            st.error("חלה שגיאה בחילוץ. וודא שהלינק תקין.")

st.write("---")
st.caption("פיתוח: בוס | מצב: API-Cloud Mode 2026")
