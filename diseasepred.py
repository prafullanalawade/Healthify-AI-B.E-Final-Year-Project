import streamlit as st
from Diabetes import diabetes_prediction_page
from Heart import heart_disease_prediction_page
from Kidney import kidney_disease_prediction_page
from streamlit_option_menu import option_menu  # Make sure you have this package installed
import os
import pickle

# Load models with error handling
working_dir = os.path.dirname(os.path.abspath(__file__))

import os
import joblib

# Update with the correct path to the model file
model_path = 'Saved_Models/best_diabetes_model.joblib'

if os.path.exists(model_path):
    diabetes_model = joblib.load(model_path)
else:
    print(f"Model file {model_path} not found.")

# Load models
working_dir = os.path.dirname(os.path.abspath(__file__))
heart_model = pickle.load(open(f'{working_dir}/Saved_Models/heart.pkl', 'rb'))
kidney_model = pickle.load(open(f'{working_dir}/Saved_Models/kindey.pkl', 'rb'))  # Add if needed

def prediction_page():
    st.title("Disease Prediction")

    # Navigation menu
    selected = option_menu(
        menu_title="Disease Prediction",  # Required
        options=["Diabetes Prediction", "Heart Disease Prediction", "Kidney Disease Prediction"],  # Options
        icons=["activity", "heart", "person"],  # Icon names (optional)
        menu_icon="hospital-fill",  # Main menu icon
        default_index=0,  # Default selected option
        orientation="horizontal"  # Display horizontally
    )

    # Handle the navigation
    if selected == "Diabetes Prediction":
        diabetes_prediction_page(diabetes_model)
    elif selected == "Heart Disease Prediction":
        heart_disease_prediction_page(heart_model)
    elif selected == "Kidney Disease Prediction":
        kidney_disease_prediction_page(kidney_model) 
    