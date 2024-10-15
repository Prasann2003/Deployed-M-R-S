import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_lottie import st_lottie


# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")  # Assuming style.css is in the same directory


# Function to load Lottie animations (for visual enhancement)
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


# Function to fetch the poster using the OMDb API
def fetch_poster(movie_title):
    api_key = '462ae3c0'
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if data['Response'] == 'True':
        return data.get('Poster')
    return None


# Function to get movie recommendations
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))
    return recommended_movies, recommended_posters


# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app UI
st.markdown('<h1 style="text-align: center; color: #FF5733;">🎬 Movie Recommender System 🍿</h1>', unsafe_allow_html=True)

# Add Lottie animation for better engagement (e.g., popcorn animation)
lottie_url = "https://assets5.lottiefiles.com/packages/lf20_sfnkt7lq.json"  # Example URL
lottie_animation = load_lottie_url(lottie_url)
if lottie_animation:
    st_lottie(lottie_animation, speed=1, width=200, height=200)

selected_movie_name = st.selectbox(
    'Choose a movie to get recommendations:',
    movies['title'].values)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)

    # Display recommended movies with posters in a stylish layout
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx < len(recommendations):
            with col:
                st.markdown(f"<h4 style='color: #33FFBD;'>{recommendations[idx]}</h4>", unsafe_allow_html=True)
                if posters[idx]:
                    st.image(posters[idx], use_column_width=True)
                else:
                    st.write("Poster not available")

    # Display a "Load More" button to show more recommendations
    if st.button('Remove Recommendations'):
        additional_recommendations, additional_posters = recommend(selected_movie_name)
        st.markdown("<h2 style='text-align: left; color: #FF5733;'>More Movies You Might Like:</h2>",
                    unsafe_allow_html=True)
        extra_cols = st.columns(5)
        for idx, col in enumerate(extra_cols):
            if idx < len(additional_recommendations):
                with col:
                    st.markdown(f"<h4 style='color: #33FFBD;'>{additional_recommendations[idx]}</h4>",
                                unsafe_allow_html=True)
                    if additional_posters[idx]:
                        st.image(additional_posters[idx], use_column_width=True)

# Add social media buttons
st.markdown('<h3 style="text-align: left; color: #FF5733;">Follow Us On</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <a href="https://www.instagram.com/prasann2003" target="_blank">
        <button style="background-color: #E1306C; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Instagram</button>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="https://www.linkedin.com/in/prasann-kumar-600467250" target="_blank">
        <button style="background-color: #0077B5; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">LinkedIn</button>
    </a>
    """, unsafe_allow_html=True)

# Footer with contact info and links
st.markdown("""
<hr style='border: 1px solid #FF5733;'>
<h5 style="text-align: center; color: #E5E5E5;">© 2024 Movie Recommender System. All Rights Reserved.</h5>
<p style="text-align: center; color: #E5E5E5;">
    For support, contact us at <a href="mailto:prasannkmr2003@gmail.com" style="color: #34ebba;">prasannkmr2003@gmail.com</a>
</p>
""", unsafe_allow_html=True)
