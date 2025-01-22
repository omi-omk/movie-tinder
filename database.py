import sqlite3
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

class Database:
    def __init__(self):
        self.database_path = 'movies.db'
        self.create_tables()

    def get_connection(self):
        return sqlite3.connect(self.database_path)

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create a table for storing movies data
        cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            genre TEXT,
            description TEXT,
            rating FLOAT,
            year INTEGER,
            director TEXT,
            actors TEXT,
            keywords TEXT,
            poster TEXT
        )''')
        
        # Create a table for storing users data
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )''')
        
        # Create a table for storing user interactions data
        cursor.execute('''CREATE TABLE IF NOT EXISTS swipes (
            user_id INTEGER,
            movie_id INTEGER,
            action TEXT,
            FOREIGN KEY (movie_id) REFERENCES movies (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
    
        conn.commit()
        conn.close()

    # Method to insert user in the db
    def add_user(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id

    # Method to select user from the db
    def get_user_id(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def get_movies(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movies')
        movies = cursor.fetchall()
        conn.close()
        return movies

    def record_swipe(self, user_id, movie_id, action):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO swipes (user_id, movie_id, action) VALUES (?, ?, ?)', 
                      (user_id, movie_id, action))
        conn.commit()
        conn.close()

    def get_recommendations(self, user_id, num_recommendations=5):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get user's liked movies
        cursor.execute('''
            SELECT m.*, s.action FROM movies m
            JOIN swipes s ON m.id = s.movie_id
            WHERE s.user_id = ? AND s.action IN ('like', 'dislike')
        ''', (user_id,))
        watched_movies = cursor.fetchall()
        if not watched_movies:
            # If no watched movies, return no recommendation.
            conn.close()
            return []
        
        # Get all movies not shown to the user and not interacted with
        cursor.execute('''
            SELECT m.*, s.action
            FROM movies m
            LEFT JOIN swipes s ON m.id = s.movie_id AND s.user_id = ?
            WHERE s.movie_id IS NULL OR s.action = 'not_seen'
        ''', (user_id,))
        unseen_movies = cursor.fetchall()
        
        if not unseen_movies:
            conn.close()
            return []

        # Create feature vectors with weighted features
        def create_feature_vector(movie):
            genres = set(g.strip() for g in movie[2].split('/'))
            mapping = { "like":1, "dislike":-3, "not_seen":0}
            return [
                mapping.get(movie[-1], 0),
                movie[4] * 2.0,  # rating (weighted more)
                (2024 - movie[5]) / 100.0,  # recency (normalized)
                1 if 'Action' in genres else 0,
                1 if 'Drama' in genres else 0,
                1 if 'Comedy' in genres else 0,
                1 if 'Sci-Fi' in genres else 0,
                1 if 'Crime' in genres else 0,
                1 if 'Thriller' in genres else 0,
                1 if 'Romance' in genres else 0,
                1 if 'Adventure' in genres else 0,
            ]

        # Prepare data for KNN
        watched_vectors = np.array([create_feature_vector(m) for m in watched_movies])
        unseen_vectors = np.array([create_feature_vector(m) for m in unseen_movies])
        
        # Standardize features
        scaler = StandardScaler()
        watched_vectors_scaled = scaler.fit_transform(watched_vectors)
        unseen_vectors_scaled = scaler.transform(unseen_vectors)
        
        # Train KNN model with more neighbors since we have more liked movies
        n_neighbors = min(5, len(watched_vectors))
        knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
        knn.fit(watched_vectors_scaled)
        
        # Get recommendations
        distances, indices = knn.kneighbors(unseen_vectors_scaled)
        
        # Calculate scores based Euclidean distance
        scores = []
        for i, movie in enumerate(unseen_movies):
            euclidean_distance = np.linalg.norm(distances[i])
            score = 1.0 / (1.0 + euclidean_distance)
            scores.append((score, movie))
        
        # Sort by score and get top recommendations
        scores.sort(reverse=True)
        recommendations = [movie for score, movie in scores[:num_recommendations]]
        
        conn.close()
        return recommendations

    def add_movie(self, title, genres, description, rating, year, director, cast, keywords, poster):
        """Add a movie to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO movies (title, genre, description, rating, year, director, actors, keywords, poster)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, genres, description, rating, year, director, cast, keywords, poster))
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding movie {title}: {str(e)}")
            return None
        finally:
            conn.close()
