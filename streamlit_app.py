import streamlit as st

# Title of App
st.title("🎶Suggestify- song recommendation app")

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 33, Web Development - Section A")
st.subheader("Elina Desai, Tamer Nawam")
# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description
#       4. **Page Name**: Description

st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. **Home Page**: You're here! 
2. **Song Recommender**: Pick a mood or vibe, and we will recommend songs using a real music API.
3. **AI DJ**: Our AI DJ writes fun intros, themed playlists, and music-based messages.
4. **Lyric Analyzer Chatbot**: Paste in your favorite lyrics and chat with our AI to explore the meaning behind the words.

""")
st.image("Images/MusicWave.jpg", caption="Find your vibe 🎵", use_container_width=True)
