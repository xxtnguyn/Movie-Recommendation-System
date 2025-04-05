import streamlit as st
import requests
import pickle
# import gdown
import os
import shutil
import numpy as np
import pandas as pd

# # Define file paths
# similarity_file_id = '14ws-qm87iDShrm9Ye_V3gqoVp-yO62Bf'
# movie_list_file_id = '1-r8sjfrPPZ-2yXQLgvh1Thd9T_Rmhwov'

# # Define file paths for output
# similarity_output = 'artifacts/similarity.pkl'
# movie_list_output = 'artifacts/movie_list.pkl'

# # Ensure the artifacts directory exists
# os.makedirs("artifacts", exist_ok=True)

# # Function to download file only if it doesn't already exist
# def download_file(file_id, output_path):
#     if not os.path.exists(output_path):  # Check if the file already exists
#         print(f"Downloading {output_path}...")
#         gdown.download(f'https://drive.google.com/uc?id={file_id}', output_path, quiet=False)
#     # else:
#     #     print(f"{output_path} already exists, skipping download.")

# # Download the .pkl files only if they don't exist
# download_file(similarity_file_id, similarity_output)
# download_file(movie_list_file_id, movie_list_output)

# files_to_remove = ["similarity.pkl", "movie_list.pkl"]
# for fname in os.listdir():
#     if any(file in fname for file in files_to_remove) and fname not in files_to_remove:
#         os.remove(fname)


# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Page title and description
st.set_page_config(page_title="Movie Recommender System", layout="wide")
st.title('🎥 Movie Recommender System')
st.markdown("""
Welcome to the **Movie Recommender System**!  
Select a movie from the dropdown below, and we'll recommend similar movies for you to enjoy.  
""")

# Load data
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🎬 Type or select a movie from the dropdown",
    movie_list
)

# Automatically show recommendations when a movie is selected
if selected_movie:
    # Fetch the selected movie's poster
    selected_movie_id = movies[movies['title'] == selected_movie].iloc[0].movie_id
    selected_movie_poster = fetch_poster(selected_movie_id)
    
    # Get recommendations
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display the selected movie
    st.markdown("### Selected Movie:")
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(selected_movie_poster, use_column_width=True)
        # Center-align the title under the image
        st.markdown(
            f"<h5 style='text-align: center; color: white;'>{selected_movie}</h5>",
            unsafe_allow_html=True
        )

    # Display recommendations in a grid layout
    st.markdown("### Recommended Movies:")
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[i], use_column_width=True)
            # Center-align the recommendation titles under the images
            st.markdown(
                f"<h5 style='text-align: center;'>{recommended_movie_names[i]}</h5>",
                unsafe_allow_html=True
            )