import streamlit as st
import requests

st.set_page_config(page_title="Audio-Tech Simple", page_icon="🎵")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 מוריד שירים פשוט ומהיר")
st.write("בלי שגיאות, בלי סיבוכים.")

url = st.text_input("הדבק לינק מיוטיוב:")

if url:
    if st.button("הורד שיר"):
        try:
            with st.spinner("מושך את השיר..."):
                # שימוש ב-API של Cobalt לעקיפת חסימות
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
                
                response = requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers)
                data = response.json()
                
                if data.get("status") == "stream" or data.get("status") == "picker":
                    download_url = data.get("url")
                    st.success("הקובץ מוכן!")
                    st.audio(download_url)
                    st.markdown(f'[📥 לחץ כאן להורדה ישירה]({download_url})')
                else:
                    st.error("לא הצלחתי למשוך את השיר. נסה לינק אחר.")
                    
        except Exception as e:
            st.error(f"שגיאה: {e}")

st.caption("פשוט, קל, עובד. בוס.")
