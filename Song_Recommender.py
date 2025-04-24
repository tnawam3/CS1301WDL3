import streamlit as st
import requests
import matplotlib.pyplot as plt

st.title("🎧 Song Recommender")
st.write("Pick a mood or artist and we'll recommend songs using iTunes!")


mood = st.selectbox("Choose a mood", ["Happy", "Sad", "Chill", "Party"])
custom_artist = st.text_input("Or enter an artist you like")


mood_map = {
    "Happy": "feel good pop",
    "Sad": "sad acoustic",
    "Chill": "lofi chill",
    "Party": "dance hits"
}

search_term = custom_artist if custom_artist else mood_map[mood]


if st.button("Get Recommendations"):
    url = f"https://itunes.apple.com/search?term={search_term}&entity=song&limit=5"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        
        if results:
            st.success(f"Top songs for '{search_term}' 🎶")
            song_names = []
            popularity_scores = []

            for item in results:
                track = item.get("trackName", "Unknown")
                artist = item.get("artistName", "Unknown")
                artwork = item.get("artworkUrl100", "")
                preview = item.get("previewUrl", "")

                st.image(artwork, width=100)
                st.markdown(f"**{track}** by *{artist}*")
                if preview:
                    st.audio(preview, format="audio/mp4")

                song_names.append(track)
                popularity_scores.append(len(track) * 5 % 100)  

            
            if st.button("Show Song Popularity Chart"):
                fig, ax = plt.subplots()
                ax.bar(song_names, popularity_scores)
                ax.set_ylabel("Popularity (Simulated)")
                ax.set_title(f"Songs for {search_term}")
                st.pyplot(fig)
        else:
            st.warning("No songs found. Try a different artist or mood.")
    else:
        st.error("Something went wrong with the API request.")


