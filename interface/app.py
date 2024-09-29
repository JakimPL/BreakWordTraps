import streamlit as st
import requests
from PIL import Image



def run():
    st.set_page_config(layout="wide")
    st.title("Predicting the quality of a wine :wine_glass:")
    st.markdown("This app uses a Random Forest regression model to predict the \
                quality of a wine based on its characteristics. \
                The most important properties are presented at the top \
                whilst the rest is included in the expandable section.")
    st.markdown("The quality of a wine is rated between 1 and 10, with higher values\
                suggesting a higher quality.")
    st.markdown("Select specific values for the characteristics below:")
    
    with st.container():
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            alcohol = st.slider(label="Alcohol",
                                min_value=8.0, max_value=15.0, step=0.1, value=10.0,
                                key="alcohol")
        with col2:
            sulphates = st.slider(label="Sulphates",
                                min_value=0.3, max_value=2.0, step=0.01, value=0.65,
                                key="sulphates")
        with col3:
            citric_acid = st.slider(label="Citric acid",
                                min_value=0.0, max_value=1.0, step=0.01, value=0.27,
                                key="citric_acid")
        with col4:
            volatile_acidity = st.slider(label="Volatile acidity",
                                min_value=0.12, max_value=1.58, step=0.01, value=0.53,
                                key="volatile_acidity")

    
    with st.container():
        with st.expander("See additional characteristics"):
            col1b, col2b, col3b, col4b = st.columns(4)
            with col1b:
                sulf_diox = st.slider(label="Total sulfur dioxide",
                                    min_value=1, max_value=500, step=1, value=45,
                                    key="total_sulfur_dioxide")
                pH = st.slider(label="pH",
                                    min_value=2.7, max_value=4.01, step=0.01, value=3.3,
                                    key="ph")              
            with col2b:
                free_sulf_diox = st.slider(label="Free sulfur dioxide",
                                min_value=1, max_value=68, step=1, value=15,
                                key="free_sulf_diox")
                density = st.slider(label="Density",
                                min_value=0.99, max_value=1.03, step=0.001, value=0.99,
                                key="density")              
            with col3b:
                chlorides = st.slider(label="Chlorides",
                                min_value=0.01, max_value=0.62, step=0.001, value=0.086,
                                key="chlorides")
                residual_sugar = st.slider(label="Residual sugar",
                                min_value=0.9, max_value=15.5, step=0.1, value=2.53, 
                                key="residual_sugar")               
            with col4b:
                fixed_acidity = st.slider(label="Fixed acidity",
                                min_value=4.6, max_value=15.9, step=0.1, value=8.31,
                                key="fixed_acidity")
    
  
    if st.button("Predict"):
        # response = requests.post("http://backend:8000/predict", json=data) #127.0.0.1
        response = requests.post("https://test-hackyeah-1-687682783908.europe-west1.run.app/hello")
        response.raise_for_status()
        prediction = response.json()
    
if __name__ == "__main__":
    run()