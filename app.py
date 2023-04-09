import streamlit as st
import pickle
import pandas as pd
import requests

# Load data and models
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Define function to fetch movie poster from API
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=ae2faada324102c8b6b0373e08403ad8')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# Define function to get recommendations
def recommend(movie, num_recommendations):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_recommendations+1]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Set page config and style
st.set_page_config(page_title='Movie Recommendation System', page_icon=':movie_camera:', layout='wide')
st.markdown("""
<style>
body {
    background-color: #F8F8F8;
}
.stButton button {
    background-color: #61C9A8;
    color: #FFFFFF;
    font-weight: bold;
    border-radius: 5px;
    border: none;
}
.stButton button:hover {
    background-color: #2D998F;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Set title and subtitle
st.title('Movie Recommendation System')
st.subheader('Get personalized movie recommendations based on your favorite movies!')



# Create slider for selecting number of recommendations to display
num_recommendations = st.slider('Number of recommendations', 1, 10, 5)

# Create dropdown for selecting a movie
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

# Create recommendation button
if st.button('Get recommendations'):
    # Get recommendations
    names, posters = recommend(selected_movie_name, num_recommendations)

    # Create columns for displaying recommendations
    cols = st.columns(num_recommendations)
    for i, col in enumerate(cols):
        col.text(names[i])
        col.image(posters[i], use_column_width=True)

# Create footer with data source
st.markdown("""
<style>
.footer {
    text-align: center;
    font-size: 12px;
    color: #555555;
    margin-top: 50px;
}
.footer a {
    color: #61C9A8;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="footer">Data source: <a href="https://www.kaggle.com/tmdb/tmdb-movie-metadata">TMDB 5000 Movie Dataset</a></div>', unsafe_allow_html=True)
