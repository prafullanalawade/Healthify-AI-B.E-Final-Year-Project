import streamlit as st
from streamlit_folium import st_folium
from loginreg import login_page, register_page, forgot_password_page, reset_password_page
from diseasepred import prediction_page
from loginreg import init_db  # Ensure init_db is imported
from streamlit_option_menu import option_menu
from logout import logout_page
from chatbot import chatbot
from visualisation import diabetes_visualization_page
from heartvisualization import heart_visualization_page
from kidneyvisualization import kidney_visualization_page
from contact import contact
from location import get_nearby_locations
from streamlit_lottie import st_lottie
import requests
from youtube import youtube_video_page


st.set_page_config(
        page_title="Healthify-AI",
        page_icon="🏥",
        layout="wide"
)

def load_lottie_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except:
        return None
    

def main():
    # Initialize the database when the app starts
    init_db()  # This will create the table if it doesn't exist

    # Initialize session state variables if not present
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False  # Initialize session state for logged_in flag

    if 'prediction_type' not in st.session_state:
        st.session_state['prediction_type'] = None  # Initialize session state for prediction type (diabetes, heart disease, etc.)
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = None  # Initialize session state for user data

    # Create a sidebar menu with buttons for each option
    with st.sidebar:
        st.markdown("<h1 class='css-1d391kg'>Healthify-AI</h1>", unsafe_allow_html=True)
        selected_option = option_menu(
            menu_title="",  # Required
            options=["Home", "Register/Login", "Diseases Prediction","Visualisation", "Personal AI Assistant","Health Video Suggestions","Nearby Clinics and Hospitals","Contact Us","Logout"],  # Required
            icons=["house-fill", "person-circle", "activity","bar-chart-fill", "robot","play-circle","geo-alt","envelope-fill","box-arrow-right"],  # Optional: add icons for each option
            menu_icon="cast",  # Optional: icon for the menu
            default_index=0,  # Default selected option
            orientation="vertical",  # Ensures buttons are stacked vertically
            styles={
                "container": {"padding": "5!important", "background-color": 'black'},
                "icon": {"color": "white", "font-size": "23px"},
                "nav-link": {
                    "color": "white",
                    "font-size": "20px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "blue",
                },
                "nav-link-selected": {"background-color": "#02ab21"},
            }
        )

        

    # Logic for handling selected options
    if selected_option == "Home":
        st.title("🌟 Welcome to Healthify-AI 🌟")
        st.write("## Your AI-powered application for better health!")
        
        # Adding an animated Lottie file
        lottie_url = "https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json"
        lottie_animation = load_lottie_url(lottie_url)

        if lottie_animation:
            st_lottie(lottie_animation, height=300, key="health_animation")

        st.markdown(
            """
            ### What can you do here?
            - Predict **Diabetes**, **Heart Disease**, and **Kidney Disease** with AI models.  
            - Get **visual insights** into your health data.  
            - Consult our **AI-powered chatbot** for quick health tips. 
            - Watch **health-related videos** to stay informed. 
            - Find **clinics and hospitals** near your location effortlessly.  

            💡 *Stay proactive and take charge of your health with Healthify-AI!*
            """
        )
        
   # Integrate Google Authentication inside "Register/Login"
    elif selected_option == "Register/Login":
        if st.session_state.get('logged_in', False):
            st.warning("You are already logged in! You can go to the Prediction page.")
        else:
            st.title("Register or Login")
            
            # Lottie URLs for animations
            lottie_register = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_3rwasyjy.json")
            lottie_login = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_xlmz9xwm.json")
            lottie_forgot = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_ehe6txyh.json")

            # Traditional login system
            login_option = st.selectbox("Choose an option", ["Register", "Login", "Forgot Password"])

            if login_option == "Register":
                if lottie_register:
                    st_lottie(lottie_register, height=250, key="register")
                    st.subheader("Register Page")
                    register_page()

            elif login_option == "Login":
                if lottie_login:
                    st_lottie(lottie_login, height=250, key="login")
                    st.subheader("Login Page")
                    login_page()  # The login_page function should set st.session_state['logged_in'] = True on successful login

            elif login_option == "Forgot Password":
                if lottie_forgot:
                    st_lottie(lottie_forgot, height=250, key="forgot")
                st.subheader("Forgot Password")
                forgot_password_page()
                reset_password_page()

        
    elif selected_option == "Diseases Prediction":
        if st.session_state['logged_in']:
            prediction_page()  # Show disease prediction page
        else:
            st.warning("Please log in to access the medicine search page.")  # Show warning if not logged in
            
    elif selected_option == "Visualisation":
        if st.session_state['logged_in']:
            # Check if prediction type is available (Diabetes, Heart Disease, or Kidney Disease)
            if st.session_state['prediction_type'] is None:
                st.warning("No prediction has been made yet. Please predict a disease first.")  # Clear warning if no prediction type
            elif st.session_state['prediction_type'] == 'diabetes':
                diabetes_visualization_page()  # Show diabetes visualization
            elif st.session_state['prediction_type'] == 'heart_disease':
                heart_visualization_page()  # Show heart disease visualization
            elif st.session_state['prediction_type'] == 'kidney':
                kidney_visualization_page()  # Show kidney disease visualization
        else:
            st.warning("Please log in to access the visualization page.")
       
    
    elif selected_option == "Personal AI Assistant":
        if st.session_state['logged_in']:
        
            # Show chatbot functionality
            chatbot()  # Call the chatbot function you have defined
        else:
            st.warning("Please log in to access the health chatbot page.")
    
    elif selected_option == "Nearby Clinics and Hospitals":
        if not st.session_state.get('logged_in', False):
            st.warning("Please log in to access the Nearby Clinics and Hospitals page.")

        else:
        # Streamlit app logic
            st.title("Find Nearby Clinics and Hospitals")

        if 'map_html' not in st.session_state:
            st.session_state.map_html = None
        if 'places' not in st.session_state:
            st.session_state.places = None

        # Input for location name
        current_location = st.text_input("Enter your current location :")
        radius = st.slider("Select search radius (meters):", 500, 5000, 1000)

        if st.button("Find Nearby clinics and hospitals"):
            if current_location.strip():
                # Call the function to get nearby locations
                map_html, places = get_nearby_locations(current_location, radius)

                if map_html:
                    # Save map and places in session state
                    st.session_state.map_html = map_html
                    st.session_state.places = places
                    st.success("Nearby locations found!")
                else:
                    st.error("Error fetching nearby locations.")
            else:
                st.warning("Please enter a valid location.")

        # Display the map and places if they exist in session state
        if st.session_state.map_html:
            st.write("### Map of Nearby Locations")
            st_folium(st.session_state.map_html, width=700, height=500)

            # Display the list of places
            if st.session_state.places:
                st.write("### List of Nearby Locations")
                for place in st.session_state.places:
                    st.write(f"**Name:** {place['name']}")
                    st.write(f"**Address:** {place['address']}")
                    st.write(f"**Contact:** {place['contact']}")
                    st.write("---")
                    
    elif selected_option == "Health Video Suggestions":
        if st.session_state['logged_in']:
            youtube_video_page()
             
        else:
            st.warning("Please log in to access the video suggestion  page.")  # Show warning if not logged in
    
    
             
    elif selected_option == "Contact Us":
        if st.session_state['logged_in']:
            contact()  # Show disease prediction page
        else:
            st.warning("Please log in to access the contact page.")  # Show warning if not logged in

    elif selected_option == "Logout":
        if st.session_state['logged_in']:
            logout_page()
            st.experimental_rerun()
        else:
            st.warning("Please log in to access the contact page.")  # Show warning if not logged in
if __name__ == "__main__":
    main()