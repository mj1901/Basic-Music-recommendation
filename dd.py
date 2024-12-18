import streamlit as st
import requests
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import speech_recognition as sr

# Load your dataset
music_data = pd.read_csv('data_moods.csv')

# Your existing backend code for vectorization and similarity calculation
selected_features = ['name', 'album', 'artist', 'id']
for feature in selected_features:
    music_data[feature] = music_data[feature].fillna('')

combined_features = music_data['name'] + ' ' + music_data['album'] + ' ' + music_data['artist'] + ' ' + music_data['id'].astype(str)
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)

# Function to fetch song album cover URL
def fetch_album_cover(song_id):
    # You need to implement this function based on your data source
    pass

# Function to perform voice search
def perform_voice_search():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please say the name of the song:")
        audio = r.listen(source)

    try:
        song_name = r.recognize_google(audio)
        return song_name
    except sr.UnknownValueError:
        st.write("Sorry, I could not understand your audio.")
    except sr.RequestError as e:
        st.write("Could not request results from Google Speech Recognition service; {0}".format(e))

# Set page config
st.set_page_config(page_title="MelodyMatinee", page_icon="🎵", layout="wide")

# Add the background image link
background_image = "https://wallpaperaccess.com/full/1188395.jpg"

# List of background images
background_images = [
    "https://cdn.wallpapersafari.com/42/53/1ZI8kB.gif",
    "https://wallpapercg.com/media/ts_2x/17157.webp",
    "https://windowscustomization.com/wp-content/uploads/2019/01/Winter-Wonder.gif",
    "https://media.tenor.com/0uDfc8UDPVMAAAAd/anime-rain.gif"
]

# Set the background images using CSS
background_images_css = "url('" + "'), url('".join(background_images) + "')"
st.markdown(
    f"""
    <style>
        body {{
            background-size: cover;
            animation: changeBackground 16s linear infinite; /* 4 images, 4 seconds each */
        }}
        
        @keyframes changeBackground {{
            0% {{
                background-image: url('{background_images[0]}');
            }}
            25% {{
                background-image: url('{background_images[1]}');
            }}
            50% {{
                background-image: url('{background_images[2]}');
            }}
            75% {{
                background-image: url('{background_images[3]}');
            }}
            100% {{
                background-image: url('{background_images[0]}');
            }}
        }}

        .stApp {{
            background: rgba(0, 0, 0, 0.8);
            color: white;
        }}
        .st-ke {{
            color: white;
        }}
        .st-cu {{
            color: white;
        }}
        .st-el {{
            color: white;
        }}
        .st-ek {{
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content
st.sidebar.image("newimg.jpeg", width=250)
st.sidebar.title("Navigation")
# Sidebar navigation
selected_page = st.sidebar.radio("Go to", ["Song Recommendations"])

# Song Recommendations Page
st.title("🎵 Song Recommendations 🎧")

# Perform voice search
if st.button("🎙️ Voice Search"):
    selected_song_voice = perform_voice_search()
    if selected_song_voice:
        st.text(f"Voice Search Result: {selected_song_voice}")
        selected_song = selected_song_voice

# Your existing code for song recommendations and display
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "33ab6ac1164e43e381821649f2349122"
CLIENT_SECRET = "826dccf2187e4061a71dc45a5b50823a"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist):
    search_query = f"track:{song_name} artist:{artist}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    # Check if the voice-searched song is in the music list
    if song not in music_data['name'].values:
        st.warning(f"No match found for the voice-searched song '{song}'.")
        return [], []

    index = music_data[music_data['name'] == song].index[0]
    distances = cosine_similarity(similarity[index:index+1], similarity).flatten()
    recommended_indices = distances.argsort()[:-6:-1]
    recommended_music_names = []
    recommended_music_posters = []
    for i in recommended_indices:
        # fetch the song poster
        artist = music_data.iloc[i]['artist']
        recommended_music_posters.append(get_song_album_cover_url(music_data.iloc[i]['name'], artist))
        recommended_music_names.append(music_data.iloc[i]['name'])

    return recommended_music_names, recommended_music_posters

music_list = music_data['name'].values

# Check if selected_song is defined or use the first song by default
selected_song = selected_song if 'selected_song' in locals() else music_list[0]

selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list,
    index=music_list.tolist().index(selected_song)
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])
    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])
