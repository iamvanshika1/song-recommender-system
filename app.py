import streamlit as st
import pickle
import pandas as pd

# Load the songs list and similarity data
songs_list = pickle.load(open('songs.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
songs = pd.DataFrame(songs_list)

# Recommendation function
def recommend(song):
    song_index = songs[songs['Song-Name'] == song].index[0]
    distances = similarity[song_index]
    songs_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
    recommended_songs = []
    for i in songs_list:
        recommended_songs.append(songs.iloc[i[0]]['Song-Name'])
    
    return recommended_songs

# Custom CSS for background and styling
st.markdown("""
    <style>
    body {
        background-color: #2b2d42;
        color: #edf2f4;
    }
    .reportview-container {
        background: linear-gradient(to right, #141e30, #243b55);
        padding: 1rem;
    }
    .sidebar .sidebar-content {
        background: #2b2d42;
    }
    .song-card {
        border-radius: 10px;
        padding: 10px;
        margin: 10px;
        background: #1f4068;
        color: white;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title(' Songs Recommender System')
st.markdown("""
Looking for your next favorite song?  
Just type in the name of a song you love, and we'll recommend similar ones! 🌟
""")

# song selection dropdown
selected_song_name = st.selectbox(
    ' Select a song:',
    songs['Song-Name'].values,
    help="Start typing the name of your favorite song to see recommendations."
)

# Recommendation button
if st.button('🔍 Recommend'):
    recommendations = recommend(selected_song_name)
    
    if recommendations:
        st.subheader(f"✨ songs similar to **{selected_song_name}**:")
        
        # Display recommendations in cards using columns
        cols = st.columns(3)  # Create 3 columns for a row layout
        for idx, song in enumerate(recommendations):
            with cols[idx % 3]:  # Distribute songs across columns
                st.markdown(f"""
                <div class="song-card">
                    <h4>{song}</h4>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.error("No recommendations found. Please try another song.")
