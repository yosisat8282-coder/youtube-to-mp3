import streamlit as st

st.set_page_config(page_title="Audio-Tech Pro", page_icon="🎙️")

st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; text-align: center; }
    .main-btn { 
        background: #2563eb; color: white !important; padding: 20px; 
        border-radius: 15px; text-decoration: none; display: inline-block;
        font-weight: bold; font-size: 1.2em; width: 100%; margin-top: 20px;
    }
    div[data-testid="stMarkdownContainer"] p { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Audio-Tech Pro")
st.write("מערכת חילוץ שיעורים והרצאות (גרסה יציבה)")
st.write("---")

url = st.text_input("הדבק לינק מיוטיוב כאן:", placeholder="https://youtube.com/...")

if url:
    st.write("### בחר שיטת הורדה:")
    
    # שיטה 1: שירות YouTubePP (הכי פשוט)
    y2mate_url = url.replace("youtube.com", "youtubepp.com")
    
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid #38bdf8;">
            <p><b>שיטה א': הורדה ישירה מהירה</b></p>
            <p>לחץ על הכפתור למטה, בחר בפורמט MP3 וקבל את השיעור מיד.</p>
            <a href="{y2mate_url}" target="_blank" class="main-btn">
                🚀 עבור לדף ההורדה של השיעור
            </a>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    
    # שיטה 2: שירות חלופי להרצאות ארוכות במיוחד
    loader_url = f"https://en.loader.to/api/card/?url={url}&f=mp3"
    
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid #10b981;">
            <p><b>שיטה ב': אופטימיזציה לשיעורים ארוכים מאוד</b></p>
            <p>מתאים להרצאות של שעתיים ומעלה.</p>
            <a href="{loader_url}" target="_blank" class="main-btn" style="background: #10b981;">
                📥 חילוץ שמע לשיעור ארוך
            </a>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("הערה: השימוש באתרים חיצוניים אלו מבטיח עקיפה של חסימות יוטיוב ב-2026.")
