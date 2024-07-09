import pickle
import streamlit as st
import requests
from Database import add_user, get_user

# Fetch movie poster function
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Recommend function
def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Main function for Streamlit app
def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ''

    st.title("FlickPulse")

    menu = ["Home", "Login", "SignUp"]
    if st.session_state.logged_in:
        menu.append("Recommendations")
        menu.append("Logout")

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to FlickPulse! Get your movie recommendations.")
        st.image('Logo.jpg', caption='Welcome to FlickPulse', use_column_width=True)

    elif choice == "Login":
        if st.session_state.logged_in:
            st.success(f"Already logged in as {st.session_state.username}")
            st.image('Logo.jpg', caption='Welcome to FlickPulse', use_column_width=True)
        else:
            st.subheader("Login Section")
            st.image('Logo.jpg', caption='Welcome to FlickPulse', use_column_width=True)
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type='password')
            if st.sidebar.button("Login"):
                user = get_user(username)
                if user:
                    if user[2] == password:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success(f"Welcome {username}")
                        st.experimental_rerun()
                    else:
                        st.error("Incorrect password")
                else:
                    st.error("User not found")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        if st.button("Sign Up"):
            user = get_user(new_user)
            if user:
                st.error("Username already exists")
            else:
                add_user(new_user, new_password)
                st.success("Account created successfully")
                st.info("Go to Login Menu to login")

    elif choice == "Recommendations" and st.session_state.logged_in:
        st.subheader("Movie Recommendations")
        movies = pickle.load(open('movie_list.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))

        movie_list = movies['title'].values
        selected_movie = st.selectbox(
            "Type or select a movie from the dropdown",
            movie_list
        )

        if st.button('Show Recommendation'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)
            columns = st.columns(5)
            for i in range(5):
                with columns[i]:
                    st.text(recommended_movie_names[i])
                    st.image(recommended_movie_posters[i])
            columns = st.columns(5)
            for i in range(5, 10):
                with columns[i - 5]:  # Adjusting index to use the same columns
                    st.text(recommended_movie_names[i])
                    st.image(recommended_movie_posters[i])

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ''
        st.success("You have been logged out")
        st.experimental_rerun()


if __name__ == '__main__':
    main()
