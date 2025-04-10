import streamlit as st
from helper import generate_pdf, send_email
from PIL import Image
import matplotlib.pyplot as plt

def heart_disease_prediction_page(heart_model):
    st.title("Heart Disease Prediction Using Machine Learning")
    image = Image.open('heart2.jpg')
    st.image(image, caption='Heart Disease Prediction')
    col1, col2 = st.columns(2)

    with col1:
        trestbps = st.number_input(
            "Resting Blood Pressure (50 - 200 mm Hg)", 
            min_value=50, 
            max_value=200, 
            step=1
        )
    with col2:
        chol = st.number_input(
            "Serum Cholesterol (126-564 mg/dl)", 
            min_value=126, 
            max_value=564, 
            step=1
        )
    with col1:
        thalach = st.number_input(
            "Maximum Heart Rate Achieved (50-220)", 
            min_value=50, 
            max_value=220, 
            step=1
        )
    with col2:
        fbs = st.number_input(
            "Fasting Blood Sugar > 120 mg/dl (0 = False, 1 = True)", 
            min_value=0, 
            max_value=1, 
            step=1
        )
    with col1:
        exang = st.number_input(
            "Exercise Induced Angina (0 = No, 1 = Yes)", 
            min_value=0, 
            max_value=1, 
            step=1
        )
    with col2:
        slope = st.number_input(
            "Slope of Peak Exercise ST Segment (0-2)", 
            min_value=0, 
            max_value=2, 
            step=1
        )
    with col1:
        ca = st.number_input(
            "Major Vessels Colored by Fluoroscopy (0-4)", 
            min_value=0, 
            max_value=4, 
            step=1
        )
    with col2:
        thal = st.number_input(
            "Thalassemia (0-3)", 
            min_value=0, 
            max_value=3, 
            step=1
        )

    if st.button("Heart Disease Test Result"):
        try:
            with st.spinner("Processing..."):
                # Input features for the model
                user_input = [trestbps, chol, thalach, fbs, exang, slope, ca, thal]

                # Model Prediction
                prediction = heart_model.predict([user_input])
                heart_result = (
                    "The person may have heart disease" if prediction[0] == 1 else "The person does not have heart disease"
                )
                st.success(heart_result)

                # Save input data for visualization
                st.session_state['user_data'] = {
                    "Resting Blood Pressure": trestbps,
                    "Serum Cholesterol": chol,
                    "Maximum Heart Rate Achieved": thalach,
                    "Fasting Blood Sugar": fbs,
                    "Exercise Induced Angina": exang,
                    "Slope of Peak Exercise ST Segment": slope,
                    "Major Vessels Colored by Fluoroscopy": ca,
                    "Thalassemia": thal,
                    "Prediction": heart_result
                }

                # Set prediction type for visualization page
                st.session_state['prediction_type'] = 'heart_disease'  # Set prediction type

                # Precautions
                if prediction[0] == 1:
                    precautions = [
                        "1. Maintain a low-sodium, heart-healthy diet.",
                        "2. Engage in moderate physical activity.",
                        "3. Avoid smoking and limit alcohol consumption.",
                        "4. Consult a cardiologist for further evaluation and treatment."
                    ]
                else:
                    precautions = ["Maintain a healthy lifestyle and regular check-ups to prevent heart disease."]

                # Display Precautions
                st.subheader("Precautions: ")
                for precaution in precautions:
                    st.write(precaution)

                # Generate the PDF
                pdf_path = generate_pdf(
                    st.session_state['user_email'], {
                        "Resting Blood Pressure": trestbps,
                        "Serum Cholesterol": chol,
                        "Maximum Heart Rate Achieved": thalach,
                        "Fasting Blood Sugar": fbs,
                        "Exercise Induced Angina": exang,
                        "Slope of Peak Exercise ST Segment": slope,
                        "Major Vessels Colored by Fluoroscopy": ca,
                        "Thalassemia": thal
                    }, heart_result, precautions, "Heart Disease"
                )

                # Display the PDF in the app
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download Your Report",
                        data=pdf_file,
                        file_name="Heart_Disease_Report.pdf",
                        mime="application/pdf",
                    )

                # Send the report via email
                send_email(
                    recipient_email=st.session_state['user_email'],
                    subject="Your Heart Disease Prediction Report",
                    body=f"Dear {st.session_state['user_email']},<br><br>Your heart disease prediction report is attached.<br>Best regards,<br>Healthify-AI Team.",
                    attachment_path=pdf_path,
                )
                st.success("Report sent to your email!")

                
        except Exception as e:
            st.error(f"An error occurred during the prediction process: {str(e)}")
