# Importing the needed libraries
import streamlit as st
import pickle
import pandas as pd
import requests

# Function for fetching the poster for the recommended movies for user's favourite movies


def fetch_poster(movie_id):
    response = requests.get(
       'https://api.themoviedb.org/3/movie/{}?api_key=979865bc02ea29d3ed091412f31b8c2b&language=en-US'.format(
           movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# Function in which the selected movie by user is processed by mapping its id
# After that finding vectors of 5 movies with the lowest cosine distance between them
# Function will return name of movie,director and poster
def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_director = []

    for i in movies_list:
        movies_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].original_title)
        recommended_movies_posters.append(fetch_poster(movies_id))
        recommended_movies_director.append(movies.iloc[i[0]].director)
    return recommended_movies, recommended_movies_posters, recommended_movies_director


# Taking .pkl file in which all names of all movies are available
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Taking .pkl file in which all similarity vectors are available
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Giving title to the web app page
st.title('Movie Recommender System')

# Designing a refining search bar for selecting a movie with a small msg on previous line
selected_movie_name = st.selectbox('Select your favourite movie!', movies['original_title'].values)


# Making different cards of recommended movies with posters along with their names and director's names
if st.button('Recommend'):
    names, posters, director = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    # Using for loop to show 5 recommended movies with the sequence poster image,name,director's name
    for y, col in enumerate(st.columns(5)):
        with col:
            st.image(posters[y])
            st.write('Movie name:')
            st.text(names[y])
            st.write('Director:')
            st.text(director[y])
