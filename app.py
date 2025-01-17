import pickle
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    return None

movies = pickle.load(open("C:/Users/Dareen/OneDrive/Desktop/recomindation/data.pkl", 'rb'))
similarity = pickle.load(open("C:/Users/Dareen/OneDrive/Desktop/recomindation/similarity.pkl", 'rb'))
movies_list = movies['title'].values

@app.route('/')
def home():
    return render_template("index.html", movies_list=movies_list)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form.get('movie')
    if movie:
        # Get the movie index from the list
        index = movies[movies['title'] == movie].index[0]
        
        # Get the similarity scores and sort them
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        
        # Initialize lists for recommended movie names and posters
        recommend_movie = []
        recommend_poster = []
        
        # Fetch recommended movies and their posters
        for i in distance[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            recommend_poster.append(fetch_poster(movie_id))
        
        # Zip the movie names and posters
        recommendations = list(zip(recommend_movie, recommend_poster))
        
        # Render the recommendations page
        return render_template('recommender.html', recommendations=recommendations)



if __name__ == "__main__":
    app.run(debug=True)
