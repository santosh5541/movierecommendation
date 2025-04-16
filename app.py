import streamlit as st
import pickle
import pandas as pd

# Load the data
with open('movie_data_dict.pkl', 'rb') as f:
    movie_dict = pickle.load(f)
new_df = pd.DataFrame(movie_dict)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Recommendation function
def recommend(movie):
    if movie not in new_df['title'].values:
        return []

    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    return [new_df.iloc[i[0]].title for i in movie_list]

# Streamlit UI
st.title("🎬 Movie Recommendation System")

# Dropdown to select movie
movie_list = new_df['title'].values
selected_movie = st.selectbox("Select a movie to get recommendations", movie_list)

# Button to get recommendations
if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    if recommendations:
        st.write("Here are the top 5 recommendations:")
        for i, title in enumerate(recommendations, 1):
            st.write(f"{i}. {title}")
    else:
        st.warning("No recommendations found.")
