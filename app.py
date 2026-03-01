import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube to MP3", page_icon="🎵")
st.title("🎵 מוריד שירים מיוטיוב")

url = st.text_input("הכנס לינק מיוטיוב:")

if url:
    if st.button("הכן קובץ להורדה"):
        try:
            with st.spinner("מעבד..."):
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': 'song.%(ext)s',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                with open("song.mp3", "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                    st.download_button("לחץ כאן להורדה", f, file_name="song.mp3")
                os.remove("song.mp3")
        except Exception as e:
            st.error(f"שגיאה: {e}")
          
