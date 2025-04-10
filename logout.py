import streamlit as st

def logout_page():
    """
    Clears the session state to log out the user.
    """
    # Clear all session state values
    for key in st.session_state.keys():
        del st.session_state[key]

    # Redirect to login page or show a logged-out message
    st.success("You have been logged out successfully!")
    st.snow()
    
    st.stop()
