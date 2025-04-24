import streamlit as st
import requests
import google.generativeai as genai
import os

GEMINI_API_KEY = "AIzaSyDXGtPsT0E6opCPw-2TH9Cssh3IYjjHXnM" 
if not GEMINI_API_KEY:
    st.error("Please set the GEMINI_API_KEY environment variable.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)

st.title("🎵 Lyric Analyzer Chatbot")
st.write("Choose a mood or artist to fetch songs, select a song to fetch its lyrics, then chat with our AI to explore their meaning!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "song_data" not in st.session_state:
    st.session_state.song_data = []
if "selected_song" not in st.session_state:
    st.session_state.selected_song = None
if "lyrics" not in st.session_state:
    st.session_state.lyrics = ""

mood = st.selectbox("Choose a mood", ["Happy", "Sad", "Chill", "Party"])
custom_artist = st.text_input("Enter an artist you like")

mood_map = {
    "Happy": "feel good pop",
    "Sad": "sad acoustic",
    "Chill": "lofi chill",
    "Party": "dance hits"
}

search_term = custom_artist if custom_artist else mood_map[mood]

if st.button("Fetch Songs"):
    try:
        url = f"https://itunes.apple.com/search?term={search_term}&entity=song&limit=5"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if results:
                st.success(f"Found songs for '{search_term}' 🎶")
                st.session_state.song_data = []
                st.session_state.selected_song = None
                st.session_state.lyrics = ""
                st.session_state.chat_history = []
                for item in results:
                    track = item.get("trackName", "Unknown")
                    artist = item.get("artistName", "Unknown")
                    st.session_state.song_data.append({"track": track, "artist": artist})
            else:
                st.warning("No songs found. Try a different artist or mood.")
        else:
            st.error("Failed to fetch songs from iTunes API.")
    except Exception as e:
        st.error(f"Error fetching songs: {str(e)}")

if st.session_state.song_data:
    st.subheader("Select a Song for Lyrics")
    song_options = [f"{song['track']} by {song['artist']}" for song in st.session_state.song_data]
    selected_song_str = st.selectbox("Choose a song:", song_options)
    
    if selected_song_str != st.session_state.selected_song:
        st.session_state.selected_song = selected_song_str
        st.session_state.lyrics = ""
        st.session_state.chat_history = []

    if st.button("Fetch Lyrics") and st.session_state.selected_song:
        selected_song = next(song for song in st.session_state.song_data if f"{song['track']} by {song['artist']}" == st.session_state.selected_song)
        artist = selected_song["artist"]
        title = selected_song["track"]
        try:
            lyrics_url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
            lyrics_response = requests.get(lyrics_url)
            if lyrics_response.status_code == 200:
                lyrics_data = lyrics_response.json()
                if "lyrics" in lyrics_data:
                    st.session_state.lyrics = lyrics_data["lyrics"]
                    st.success("Lyrics fetched successfully!")
                else:
                    st.warning("Lyrics not found for this song.")
            else:
                st.error("Failed to fetch lyrics from Lyrics.ovh API.")
        except Exception as e:
            st.error(f"Error fetching lyrics: {str(e)}")

if st.session_state.lyrics:
    st.subheader("Lyrics")
    st.text(st.session_state.lyrics)

st.subheader("Chat with the Lyric Analyzer")
user_input = st.text_input("Ask about the lyrics:", key="user_input")

if user_input and st.session_state.lyrics:
    try:
        chat_history = "\n".join([f"{'User' if msg['role'] == 'user' else 'AI'}: {msg['content']}" for msg in st.session_state.chat_history[-3:]])
        prompt = f"""
        You are a Lyric Analyzer Chatbot. Your role is to answer questions about the meaning, themes, or mood of the following lyrics. Be insightful, friendly, and conversational. If the user asks unrelated questions, politely redirect them to the lyrics. Use the chat history to maintain context.

        Lyrics:
        {st.session_state.lyrics}

        Chat History:
        {chat_history}

        User Question:
        {user_input}
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        ai_response = response.text

        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        st.error(f"Error with Gemini API: {str(e)}. Please try again or check your API key.")
elif user_input and not st.session_state.lyrics:
    st.info("Please fetch lyrics for a song before chatting.")

if st.session_state.chat_history:
    st.subheader("Conversation")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You**: {msg['content']}")
        else:
            st.markdown(f"**AI**: {msg['content']}")