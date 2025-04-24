import streamlit as st
import requests
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDXGtPsT0E6opCPw-2TH9Cssh3IYjjHXnM" 
if not GEMINI_API_KEY:
    st.error("Please set the GEMINI_API_KEY environment variable.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)

st.title("🎧 AI DJ")
st.write("Choose a mood and artist, and our AI DJ will create a themed playlist introduction based on iTunes song recommendations!")

mood = st.selectbox("Choose a mood", ["Happy", "Sad", "Chill", "Party"])
custom_artist = st.text_input("Enter an artist you like")

mood_map = {
    "Happy": "feel good pop",
    "Sad": "sad acoustic",
    "Chill": "lofi chill",
    "Party": "dance hits"
}

search_term = custom_artist if custom_artist else mood_map[mood]

if st.button("Generate Playlist Intro"):
    url = f"https://itunes.apple.com/search?term={search_term}&entity=song&limit=5"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        if results:
            song_data = []
            for item in results:
                track = item.get("trackName", "Unknown")
                artist = item.get("artistName", "Unknown")
                song_data.append(f"{track} by {artist}")
            
            song_list = "\n".join(song_data)
            prompt = f"""
            You are an energetic AI DJ. Based on the following songs recommended for the mood '{mood}' and artist/search term '{search_term}', write a 150-word playlist introduction. The intro should be lively, engaging, and set the tone for a themed playlist that matches the mood. Mention the mood and at least two of the songs (including artist names) to hype up the listener. Make it sound like a radio DJ introducing a curated playlist.

            Songs:
            {song_list}
            """
            
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                intro = response.text
                
                st.subheader("AI DJ Playlist Introduction")
                st.write(intro)
            
            except Exception as e:
                st.error(f"Error generating playlist intro: {str(e)}")
        else:
            st.warning("No songs found. Try a different artist or mood.")
    else:
        st.error("Something went wrong with the iTunes API request.")