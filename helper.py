import smtplib
from fpdf import FPDF
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import config


def send_email(recipient_email, subject, body, attachment_path=None):
    
    # Use credentials from config.py
    sender_email = config.EMAIL
    sender_password = config.APP_PASSWORD


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    if attachment_path:
        with open(attachment_path, "rb") as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
            msg.attach(attachment)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def generate_pdf(email, inputs, result, precautions, disease_type):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add web app name watermark
    pdf.set_font("Arial", size=60, style="B")
    pdf.set_text_color(240, 240, 240)
    pdf.text(30, 120, "HealthifyAI")
    pdf.set_text_color(0, 0, 0)

    # Title and Result
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt=f"{disease_type} Prediction Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Prediction Result: {result}", ln=True)

    # Motivational message
    pdf.ln(10)
    if result == "The person may have diabetes" or result == "The person may have heart disease" or result == "The person may have kidney disease":
        motivational_message = (
            "You are stronger than you think! The journey to health may have its challenges, "
            "but with determination, proper care, and positivity, you can lead a fulfilling life."
        )
    else:
        motivational_message = (
            "Excellent work! Your healthy habits are paying off. Keep embracing a lifestyle "
            "that nurtures your well-being. Stay strong and healthy!"
        )
    pdf.multi_cell(0, 10, txt=motivational_message)

    # Inputs provided in a table format
    pdf.ln(10)
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(80, 10, "Input", border=1, align="C")
    pdf.cell(60, 10, "Value", border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", size=12)
    for key, value in inputs.items():
        pdf.cell(80, 10, key, border=1, align="C")
        pdf.cell(60, 10, str(value), border=1, align="C")
        pdf.ln()

    # Precautions
    pdf.ln(10)
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(200, 10, txt="Precautions:", ln=True)
    pdf.set_font("Arial", size=12)
    for precaution in precautions:
        pdf.cell(0, 10, txt=precaution, ln=True)

    file_name = f"{disease_type}_report.pdf"
    pdf.output(file_name)
    return file_name
