import streamlit as st
from transcription.statistics import Statistics
from transcription.process import TranscriptionProcessor

# Tworzenie dwóch kolumn obok siebie
col1, col2 = st.columns([1, 1])  # Ustaw proporcje kolumn, np. 1:1

# W pierwszej kolumnie wyświetlamy tekst
with col1:
    st.image("images/mflogo.png", width=100)

# W drugiej kolumnie wyświetlamy obraz
with col2:
    st.markdown("<h1 style='text-align: center; color: white;'>Video Analyzer</h1>", unsafe_allow_html=True)


video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
if video_file is not None:
    # Display the uploaded video
    st.video(video_file)
    if st.button("Process Video"):
        # Send the video file to the backend for processing
        files = {"file": video_file.getvalue()}
        response = requests.post("http://localhost:8000/process_video", files=files)

        if response.status_code == 200:
            st.success("Video processed successfully!")
            result = response.json()
            transcription_box = st.empty()
            transcription_processor = TranscriptionProcessor(result, transcription_box)
            transcription_processor.fill_transcription()
            statistics = Statistics(result)
            statistics.get_statistics()
            st.write(result)

        else:
            st.error("Error processing video. Please try again.")


# Adding a video in a beautiful frame
st.write("#### Watch the Video:")
st.markdown(
    """
    <div style='border: 2px solid #4CAF50; padding: 10px; text-align: center; border-radius: 10px; background-color: #f9f9f9;'>
        <video width="700" controls>
          <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">
          Your browser does not support the video tag.
        </video>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
st.sidebar.title("Explore the Story")
sections = ["Introduction", "Frame-by-Frame Breakdown", "Motion Analysis", "Object Detection", "Conclusion"]
selected_section = st.sidebar.radio("Go to section:", sections)

# ---- Adding dynamic "tiles" (kafelki) for each section below the video ----
st.write("## Explore the Sections Below:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Frame-by-Frame Breakdown"):
        st.header("Frame-by-Frame Breakdown")
        st.write("""
        The video is broken down frame by frame to provide a detailed analysis of what's happening at each moment.
        Below is a simulation of the frames and their corresponding data.
        """)

        # Simulated data for frames
        frames = np.arange(1, 101)
        brightness = np.random.normal(loc=100, scale=20, size=100)
        motion_level = np.random.normal(loc=50, scale=15, size=100)

        # Create a DataFrame
        df = pd.DataFrame({
            'Frame': frames,
            'Brightness': brightness,
            'Motion Level': motion_level
        })

        # Plotting Frame Brightness over time
        st.subheader("Frame Brightness over Time")
        fig, ax = plt.subplots()
        ax.plot(df['Frame'], df['Brightness'], color='blue', label='Brightness')
        ax.set_xlabel("Frame Number")
        ax.set_ylabel("Brightness")
        ax.set_title("Brightness Across Video Frames")
        st.pyplot(fig)

        # Display the DataFrame for user interaction
        st.write("### Frame Data (First 20 Frames)")
        st.dataframe(df.head(20))

with col2:
    if st.button("Motion Analysis"):
        st.header("Motion Analysis")
        st.write("""
        Motion analysis helps detect the level of activity across the video. Peaks in the motion data can indicate important scenes with significant movement.
        """)

        # Plotting Motion Level over frames
        st.subheader("Motion Levels Across Frames")
        fig, ax = plt.subplots()
        ax.plot(df['Frame'], df['Motion Level'], color='red', label='Motion Level')
        ax.set_xlabel("Frame Number")
        ax.set_ylabel("Motion Level")
        ax.set_title("Motion Level Across Video Frames")
        st.pyplot(fig)

with col3:
    if st.button("Object Detection"):
        st.header("Object Detection")
        st.write("""
        The video analysis also includes detecting objects in various frames. Below are simulated counts of objects detected in different scenes.
        """)

        # Simulated data for object detection
        scenes = np.arange(1, 11)
        object_counts = np.random.randint(1, 20, size=10)

        df_objects = pd.DataFrame({
            'Scene': scenes,
            'Objects Detected': object_counts
        })

        # Bar chart for object detection
        st.subheader("Objects Detected per Scene")
        fig, ax = plt.subplots()
        ax.bar(df_objects['Scene'], df_objects['Objects Detected'], color='green')
        ax.set_xlabel("Scene Number")
        ax.set_ylabel("Objects Detected")
        ax.set_title("Objects Detected Across Video Scenes")
        st.pyplot(fig)

        # Display object detection data
        st.write("### Object Detection Data")
        st.dataframe(df_objects)

with col4:
    if st.button("Conclusion"):
        st.header("Conclusion")
        st.write("""
        Through this video analysis, we’ve uncovered key insights into the motion, objects, and activities captured. The data offers a clear picture of the most significant moments.
        """)

        st.subheader("Key Takeaways:")
        st.markdown("""
        - **Frame-by-Frame Analysis**: Showed notable variations in brightness and motion levels.
        - **Motion Detection**: Helped us identify key scenes with significant activity.
        - **Object Detection**: Provided a clear understanding of the variety of objects present in different scenes.
        
        Thank you for following this video analysis journey!
        """)

# ---- End of section ----
