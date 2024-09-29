import streamlit as st
import requests

from transcription.statistics import Statistics
from transcription.process import TranscriptionProcessor

# Tworzenie dwóch kolumn obok siebie
col1, col2 = st.columns([1, 1])  # Ustaw proporcje kolumn, np. 1:1

# W pierwszej kolumnie wyświetlamy tekst
# with col1:
#     st.image("images/mflogo.png", width=100)

# W drugiej kolumnie wyświetlamy obraz
with col2:
    st.markdown("<h1 style='text-align: center; color: white;'>Video Analyzer</h1>", unsafe_allow_html=True)


video_file = st.file_uploader("Wgraj wideo", type=["mp4", "mov", "avi"])
if video_file is not None:
    # Display the uploaded video
    st.video(video_file)
    if st.button("Przetwórz wideo"):
        # Send the video file to the backend for processing
        files = {"file": video_file.getvalue()}
        response = requests.post("http://localhost:8000/process_video", files=files)

        if response.status_code == 200:
            st.success("Wideo przetworzono pomyślnie!")
            result = response.json()
            transcription_box = st.empty()
            transcription_processor = TranscriptionProcessor(result, transcription_box)
            transcription_processor.fill_transcription()
            statistics = Statistics(result)
            statistics.get_statistics()
            st.write(result["analysis"])

        else:
            st.error("Błąd przetwarzania wideo.")
