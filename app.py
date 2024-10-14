import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=675b3cf6135ff9a144547bdfdbf0340c&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def fetch_rating(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=675b3cf6135ff9a144547bdfdbf0340c&language=en-US'.format(
            movie_id))
    data = response.json()
    return data['vote_average']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_genres = []
    recommended_movies_ratings = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_genres.append(movies.iloc[i[0]].genres)
        recommended_movies_ratings.append(fetch_rating(movie_id))

    return recommended_movies, recommended_movies_posters, recommended_movies_genres, recommended_movies_ratings


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Add background image and custom styles
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.pexels.com/photos/3945321/pexels-photo-3945321.jpeg?auto=compress&cs=tinysrgb&w=600");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Simple yellow heading in one line */
    h1 {
        font-family: 'Verdana', sans-serif;
        font-size: 4em;
        color: #FFD700;  /* Pure yellow color */
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);  /* A soft shadow to make it pop */
        margin-bottom: 0.5em;
    }

    h2, h4 {
        animation: fadeIn 2s ease-in-out;
    }

    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px 24px;
    }

    img {
        border-radius: 15px;
        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5);
    }

    .movie-container {
        padding: 10px;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Page Title
st.markdown("<h1>Movie Recommender System</h1>", unsafe_allow_html=True)

st.markdown(
    "<h2 style='text-align: center; color: #FFD700; font-family: Arial, sans-serif; text-shadow: 1px 1px 3px black;'>Uncover Your Next Cinematic Adventure!</h2>",
    unsafe_allow_html=True)
st.markdown(
    "<h4 style='text-align: center; color: white; font-family: Arial, sans-serif;'>Select your favorite movie and let us do the magic of recommendations!</h4>",
    unsafe_allow_html=True)

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    with st.spinner('Fetching recommendations...'):
        names, posters, genres, ratings = recommend(selected_movie_name)

    cols = st.columns(5)
    for index, (name, poster, genre, rating) in enumerate(zip(names, posters, genres, ratings)):
        with cols[index % 5]:
            st.markdown(f"""
            <div class="movie-container">
                <h3>{name}</h3>
                <p style='color: gray;'>{genre}</p>
                <p style='color: gray;'>Rating: {rating}/10</p>
                <img src='{poster}' width='150'/>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <footer style='text-align: center; padding: 20px; color: white;'>
        <p>Follow me on:</p>
        <a href="https://instagram.com/prasann_choudhary29" style='color: #E1306C;'>Instagram</a> |
        <a href="https://linkedin.com/in/prasann-kumar-600467250" style='color: #0077B5;'>LinkedIn</a>
    </footer>
""", unsafe_allow_html=True)
