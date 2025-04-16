import streamlit as st
import pickle
import pandas as pd
import requests

# Load data
with open('movie_data_dict.pkl', 'rb') as f:
    movie_dict = pickle.load(f)
new_df = pd.DataFrame(movie_dict)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

API_KEY = '4800dbef9007f84ee4e462a7ece928f8'

# TMDB poster fetcher
def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation function
def recommend(movie):
    if movie not in new_df['title'].values:
        return [], []

    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        title = new_df.iloc[i[0]].title
        recommended_titles.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_titles, recommended_posters

# Page config
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #111;
        }
        .main-title {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            color: #FF4C4C;
            margin-bottom: 30px;
        }
        .movie-box {
            background-color: #1e1e1e;
            border-radius: 12px;
            padding: 15px;
            transition: transform 0.2s ease-in-out;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            text-align: center;
        }
        .movie-box:hover {
            transform: scale(1.03);
            box-shadow: 0 6px 20px rgba(255,76,76,0.3);
        }
        .movie-title {
            color: #fff;
            font-weight: bold;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">🎥 Movie Recommendation System</div>', unsafe_allow_html=True)

# Dropdown
movie_list = new_df['title'].values
selected_movie = st.selectbox("🎬 Pick a movie to get recommendations:", movie_list)

# Button
if st.button("🔍 Show Recommendations"):
    titles, posters = recommend(selected_movie)
    if titles:
        st.markdown("## 🔥 You might also like:")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.markdown(f"""
                    <div class="movie-box">
                        <img src="{posters[i]}" width="100%" style="border-radius: 10px;">
                        <div class="movie-title">{titles[i]}</div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.error("Movie not found or no similar results.")
