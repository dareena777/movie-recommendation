import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import pickle
import requests
from io import BytesIO

# Set appearance mode for CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Load movie data
movies = pickle.load(open("C:/Users/Dareen/OneDrive/Desktop/recomindation/data.pkl", 'rb'))
similarity = pickle.load(open("C:/Users/Dareen/OneDrive/Desktop/recomindation/similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Function to fetch the movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    try:
        data = requests.get(url)
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
    except Exception as e:
        print(f"Error fetching poster: {e}")
    return None

# Function to recommend movies
def recommend():
    selected_movie = movie_combobox.get()
    if not selected_movie:
        messagebox.showerror("Error", "Please select a movie!")
        return

    try:
        # Get the movie index from the list
        index = movies[movies['title'] == selected_movie].index[0]

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

        # Display recommendations
        for widget in recommendation_frame.winfo_children():
            widget.destroy()  # Clear previous recommendations

        for i in range(len(recommend_movie)):
            # Fetch and display poster
            if recommend_poster[i]:
                response = requests.get(recommend_poster[i])
                img_data = BytesIO(response.content)
                img = Image.open(img_data)
                img = img.resize((150, 225), Image.Resampling.LANCZOS)  # Use Image.Resampling.LANCZOS instead of Image.ANTIALIAS
                poster_image = ImageTk.PhotoImage(img)

                poster_label = ctk.CTkLabel(recommendation_frame, image=poster_image)
                poster_label.image = poster_image  # Keep a reference to avoid garbage collection
                poster_label.grid(row=0, column=i, padx=10, pady=5)

            # Display movie title below the poster
            title_label = ctk.CTkLabel(recommendation_frame, text=recommend_movie[i], font=("Arial", 14))
            title_label.grid(row=1, column=i, padx=10, pady=5)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Initialize the main window
app = ctk.CTk()
app.title("Movie Recommendation System")
app.geometry("800x600")

# Heading
heading_label = ctk.CTkLabel(app, text="Movie Recommendation System", font=("Arial", 20, "bold"))
heading_label.pack(pady=20)

# Movie selection
movie_label = ctk.CTkLabel(app, text="Select a movie:", font=("Arial", 16))
movie_label.pack(pady=10)

movie_combobox = ctk.CTkComboBox(app, values=movies_list, width=400)
movie_combobox.pack(pady=10)

recommend_button = ctk.CTkButton(app, text="Get Recommendations", command=recommend)
recommend_button.pack(pady=20)

# Recommendations frame
recommendation_frame = ctk.CTkFrame(app, width=750, height=400)
recommendation_frame.pack(pady=20, fill="both", expand=True)

# Run the application
app.mainloop()
