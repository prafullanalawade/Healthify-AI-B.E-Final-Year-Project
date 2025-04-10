import sqlite3
import hashlib
import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re


# Helper functions
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    sex TEXT NOT NULL,
                    weight REAL NOT NULL,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    # Regular expression for validating email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        return False

def register_user(name, age, sex, weight, email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    
    try:
        c.execute('INSERT INTO users (name, age, sex, weight, email, password) VALUES (?, ?, ?, ?, ?, ?)',
                  (name, age, sex, weight, email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("This email is already registered.")
    finally:
        conn.close()


def check_login(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute('SELECT * FROM users WHERE email=? AND password=?', (email, hashed_password))
    result = c.fetchone()
    conn.close()
    return result

def send_email(recipient_email, subject, body):
    sender_email = "healthify605@gmail.com"
    sender_password = "kgjm orbe jwrx ncxx"


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'An error occurred while sending the email: {e}')

def generate_otp():
    import random
    return random.randint(100000, 999999)

def validate_otp(input_otp, actual_otp):
    return input_otp == actual_otp

# Streamlit app pages
import streamlit as st
from loginreg import check_login  # Assuming check_login is defined in loginreg.py
def login_page():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_login(email, password):
            # On successful login, save user details to session state
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email  # Save email to session state
            st.success("Login successful! go to the Prediction page.")
            st.balloons()
            
            # Set the logged_in flag to automatically trigger the prediction page
            st.session_state['page'] = 'Prediction'  # This can be used in mainapp.py for page routing
        else:
            st.error("Invalid email or password")

def register_page():
    st.title("Register")
    
    # Collecting user details
    name = st.text_input("Name of Patient")
    age = st.number_input("Age", min_value=0, max_value=150, step=1)
    sex = st.radio("Sex", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, step=0.1)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not validate_email(email):
            st.error("Please enter a valid email address (e.g., example@domain.com).")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters long.")
        else:
            try:
                register_user(name, age, sex, weight, email, password)
                st.success("Registration successful! You can now log in.")
                st.balloons()
            except ValueError as e:
                st.error(str(e))

def forgot_password_page():
    st.title("Forgot Password")
    email = st.text_input("Enter your registered email")

    if st.button("Send OTP"):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email=?', (email,))
        result = c.fetchone()
        conn.close()

        if result:
            otp = generate_otp()
            st.session_state['otp'] = otp
            st.session_state['email_for_reset'] = email
            send_email(email, "Password Reset OTP", f"Your OTP for password reset is: {otp}")
            st.success("OTP sent to your email!")
        else:
            st.error("Email not found in our database")

    if 'otp' in st.session_state:
        user_otp = st.text_input("Enter OTP", type="password")

        if st.button("Verify OTP"):
            if validate_otp(int(user_otp), st.session_state['otp']):
                # Set session state to show reset password page after OTP verification
                st.session_state['reset_password_page'] = True
                st.success("OTP verified! You can now reset your password.")
            else:
                st.error("Invalid OTP")

def reset_password_page():
    st.title("Reset Password")
    new_password = st.text_input("Enter new password", type="password")
    confirm_password = st.text_input("Confirm new password", type="password")

    if st.button("Reset Password"):
        if new_password == confirm_password:
            hashed_password = hash_password(new_password)
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('UPDATE users SET password=? WHERE email=?', (hashed_password, st.session_state['email_for_reset']))
            conn.commit()
            conn.close()
            st.success("Password reset successful! Logging you in...")

        else:
            st.error("Passwords do not match.")


# App Navigation
def app():
    # Initialize the database
    init_db()
    
    # Control page flow
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.success(f"Welcome, {st.session_state['user_email']}!")
    else:
        option = st.sidebar.selectbox("Select Option", ["Login", "Register", "Forgot Password", "Reset Password"]) 
        if option == "Login":
            login_page()
        elif option == "Register":
            register_page()
        elif option == "Forgot Password":
            forgot_password_page()
        elif option == "Reset Password":
            reset_password_page()

# Run the app
if __name__ == "__main__":
    app()
