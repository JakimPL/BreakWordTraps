import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Video Analysis Story", layout="wide")

# Title and Introduction
st.title("Story of a Video Analysis")
st.write("""
### A Deep Dive into the Insights from Video Content
In this story, we explore the depths of video analysis using various techniques such as frame-by-frame analysis, motion detection, and object recognition.
We provide a detailed breakdown of each component of the video, offering you the most comprehensive insights possible.
""")

# Sidebar for navigation
st.sidebar.title("Explore the Story")
sections = ["Introduction", "Frame-by-Frame Breakdown", "Motion Analysis", "Object Detection", "Conclusion"]
selected_section = st.sidebar.radio("Go to section:", sections)

# Frame-by-Frame Breakdown Section
if selected_section == "Frame-by-Frame Breakdown":
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

# Motion Analysis Section
elif selected_section == "Motion Analysis":
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

# Object Detection Section
elif selected_section == "Object Detection":
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

# Conclusion Section
elif selected_section == "Conclusion":
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

