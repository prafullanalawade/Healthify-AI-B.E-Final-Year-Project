import streamlit as st
from helper import generate_pdf, send_email
from PIL import Image
import matplotlib.pyplot as plt

def kidney_disease_prediction_page(kidney_model):
    st.title("Kidney Disease Prediction Using Machine Learning")
    image = Image.open('Kidney.jpg')
    st.image(image, caption='Kidney Disease Prediction')
    col1, col2, col3 = st.columns(3)

    # Input Fields for Kidney Disease Prediction
    with col1:
        age = st.number_input("Age (18-100)", min_value=18, max_value=100, value=18)
    with col2:
        blood_pressure = st.number_input("Blood Pressure (50-200 mm Hg)", min_value=50, max_value=200, value=50)
    with col3:
        blood_sugar = st.number_input("Blood Sugar Level (>120 mg/dl)", min_value=0, max_value=1, value=0)
    with col2:
        albumin = st.number_input("Albumin (3.5-5 g/dl)", min_value=3.5, max_value=5.0, value=3.5)
    with col3:
        creatinine = st.number_input("Serum Creatinine (0.5-5 mg/dl)", min_value=0.5, max_value=5.0, value=1.0)
    with col2:
        urea = st.number_input("Blood Urea Nitrogen (7-20 mg/dl)", min_value=7.0, max_value=20.0, value=7.0)
    with col3:
        red_blood_cells = st.number_input("Red Blood Cells (0-1)", min_value=0, max_value=1, value=0)
    with col1:
        haemoglobin = st.number_input("Haemoglobin Level (10-20 g/dl)", min_value=10.0, max_value=20.0, value=10.0)

    if st.button("Kidney Disease Test Result"):
        try:
            with st.spinner("Processing..."):
                # Input features for the model
                user_input = [age, blood_pressure, blood_sugar, albumin, creatinine, urea, red_blood_cells, haemoglobin]

                # Model Prediction
                prediction = kidney_model.predict([user_input])
                kidney_result = (
                    "The person may have kidney disease" if prediction[0] == 1 else "The person does not have kidney disease"
                )
                st.success(kidney_result)

                # Save input data for visualization
                st.session_state['user_data'] = {
                    "Age": age,
                    "Blood Pressure": blood_pressure,
                    "Blood Sugar Level > 120 mg/dl": blood_sugar,
                    "Albumin": albumin,
                    "Serum Creatinine": creatinine,
                    "Blood Urea Nitrogen": urea,
                    "Red Blood Cells": red_blood_cells,
                    "Haemoglobin Level": haemoglobin,
                    "Prediction": kidney_result
                }

                # Set prediction type for visualization page
                st.session_state['prediction_type'] = 'kidney_disease'  # Set prediction type

                # Precautions
                if prediction[0] == 1:
                    precautions = [
                        "1. Maintain a low-sodium, kidney-friendly diet.",
                        "2. Keep your blood pressure under control.",
                        "3. Avoid excessive protein intake.",
                        "4. Stay hydrated, but avoid excess fluid intake if advised by a doctor.",
                        "5. Consult a nephrologist for a detailed evaluation and treatment plan."
                    ]
                else:
                    precautions = ["Maintain a healthy lifestyle and regular check-ups to prevent kidney disease."]

                # Display Precautions
                st.subheader("Precautions: ")
                for precaution in precautions:
                    st.write(precaution)

                # Generate the PDF
                pdf_path = generate_pdf(
                    st.session_state['user_email'], {
                        "Age": age,
                        "Blood Pressure": blood_pressure,
                        "Blood Sugar Level > 120 mg/dl": blood_sugar,
                        "Albumin": albumin,
                        "Serum Creatinine": creatinine,
                        "Blood Urea Nitrogen": urea,
                        "Red Blood Cells": red_blood_cells,
                        "Haemoglobin Level": haemoglobin
                    }, kidney_result, precautions, "Kidney Disease"
                )

                # Display the PDF in the app
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download Your Report",
                        data=pdf_file,
                        file_name="Kidney_Disease_Report.pdf",
                        mime="application/pdf",
                    )

                # Send the report via email
                send_email(
                    recipient_email=st.session_state['user_email'],
                    subject="Your Kidney Disease Prediction Report",
                    body=f"Dear {st.session_state['user_email']},<br><br>Your kidney disease prediction report is attached.<br>Best regards,<br>Healthify-AI Team.",
                    attachment_path=pdf_path,
                )
                st.success("Report sent to your email!")

                

        except Exception as e:
            st.error(f"An error occurred during the prediction process: {str(e)}")
