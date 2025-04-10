import streamlit as st
from helper import generate_pdf, send_email
from PIL import Image
import matplotlib.pyplot as plt


def diabetes_prediction_page(diabetes_model):
    st.title("Diabetes Prediction Using Machine Learning")
    image = Image.open('d3.jpg')
    st.image(image, caption='Diabetes Disease Prediction')
    col1, col2 = st.columns(2)

    with col1:
        Glucose = st.number_input("Enter your Glucose Level (0-200)", min_value=0, max_value=200, step=1)
    with col2:
        BloodPressure = st.number_input("Enter Your Blood Pressure Value (0-110)", min_value=0, max_value=110, step=1)
    with col1:
        Insulin = st.number_input("Enter Your Insulin Level In Body (0-850)", min_value=0, max_value=850, step=1)
    with col2:
        BMI = st.number_input("Enter Your Body Mass Index/BMI Value (0-70)", min_value=0, max_value=70, step=1)
    with col1:
        Age = st.number_input("Enter Your Age (20-80)", min_value=20, max_value=80, step=1)

    if st.button("Diabetes Test Result"):
        try:
            with st.spinner("Processing..."):
                # Input features for the model
                user_input = [Glucose, BloodPressure, Insulin, BMI, Age]

                # Model Prediction
                prediction = diabetes_model.predict([user_input])
                diabetes_result = "The person may have diabetes" if prediction[0] == 1 else "The person has no diabetes"
                st.success(diabetes_result)

                # Save input data for visualization
                st.session_state['user_data'] = {
                    "Glucose Level": Glucose,
                    "Blood Pressure Value": BloodPressure,
                    "Insulin Value": Insulin,
                    "BMI Value": BMI,
                    "Age": Age,
                    "Prediction": diabetes_result
                }

                # Set prediction type for visualization page
                st.session_state['prediction_type'] = 'diabetes'  # Set prediction type

                # Precautions
                if prediction[0] == 1:
                    precautions = [
                        "1. Follow a healthy, balanced diet low in sugar.",
                        "2. Engage in regular physical exercise.",
                        "3. Monitor blood glucose levels frequently.",
                        "4. Consult a healthcare professional for further advice."
                    ]
                else:
                    precautions = ["Maintain a healthy lifestyle and regular check-ups."]

                # Display Precautions
                st.subheader("Precautions: ")
                for precaution in precautions:
                    st.write(precaution)

                # Generate the PDF
                pdf_path = generate_pdf(
                    st.session_state['user_email'], {
                        "Glucose Level": Glucose,
                        "Blood Pressure Value": BloodPressure,
                        "Insulin Value": Insulin,
                        "BMI Value": BMI,
                        "Age": Age
                    }, diabetes_result, precautions, "Diabetes"
                )

                # Display the PDF in the app
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download Your Report",
                        data=pdf_file,
                        file_name="Diabetes_Report.pdf",
                        mime="application/pdf",
                    )

                # Send the report via email
                send_email(
                    recipient_email=st.session_state['user_email'],
                    subject="Your Diabetes Prediction Report",
                    body=f"Dear {st.session_state['user_email']},<br><br>Your diabetes prediction report is attached.<br>Best regards,<br>Healthify-AI Team.",
                    attachment_path=pdf_path,
                )
                st.success("Report sent to your email!")


        except Exception as e:
            st.error(f"An error occurred during the prediction process: {str(e)}")
