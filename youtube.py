import streamlit as st
import requests

# Function to fetch YouTube videos
def fetch_youtube_videos(query):
    API_KEY = "AIzaSyD_E43dxIrj7M9pVtBrs3z3erbKlnnJqcY"  # Replace with your actual API Key
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "maxResults": 30,  # Get top 10 results
        "q": query,
        "key": API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        if "items" in data:
            return data["items"]
        else:
            st.warning("No videos found for this query.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching videos: {e}")
        return []

# Function to display videos
def youtube_video_page():
    st.title("Health Video Suggestions")
    
    query = st.text_input("Enter a health topic to search for videos:")
    
    if st.button("Search"):
        if query.strip():
            videos = fetch_youtube_videos(query)
            
            if videos:
                for video in videos:
                    video_title = video["snippet"]["title"]
                    video_description = video["snippet"]["description"]
                    video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                    thumbnail_url = video["snippet"]["thumbnails"]["high"]["url"]

                    # Display video with description and thumbnail
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.image(thumbnail_url, width=150)
                    with col2:
                        st.markdown(f"### [{video_title}]({video_url})")
                        st.write(f"**Description:** {video_description}")
                    st.write("---")
        else:
            st.warning("Please enter a search term.")

