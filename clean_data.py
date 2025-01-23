import sqlite3
import os

def clean_database():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    # Get all movies
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    
    # Default values for missing data
    defaults = {
        'title': 'Unknown Title',
        'genre': 'Uncategorized',
        'description': 'No description available',
        'rating': 0.0,
        'year': 0,
        'director': 'Unknown Director',
        'actors': 'Unknown Cast',
        'keywords': '',
        'poster': 'default_poster.webp'
    }
    
    # Clean each movie
    for movie in movies:
        movie_id = movie[0]
        cleaned_values = []
        
        # Clean each field
        title = movie[1] if movie[1] else defaults['title']
        genre = movie[2] if movie[2] else defaults['genre']
        description = movie[3] if movie[3] else defaults['description']
        rating = float(movie[4]) if movie[4] is not None else defaults['rating']
        year = int(movie[5]) if movie[5] is not None else defaults['year']
        director = movie[6] if movie[6] else defaults['director']
        actors = movie[7] if movie[7] else defaults['actors']
        keywords = movie[8] if movie[8] else defaults['keywords']
        poster = movie[9] if movie[9] and os.path.exists(f'static/posters/{movie[9]}') else defaults['poster']
        
        # Update the movie with cleaned values
        cursor.execute('''
            UPDATE movies 
            SET title=?, genre=?, description=?, rating=?, year=?, director=?, actors=?, keywords=?, poster=?
            WHERE id=?
        ''', (title, genre, description, rating, year, director, actors, keywords, poster, movie_id))
    
    # Remove any movies with default titles (likely completely empty entries)
    cursor.execute('DELETE FROM movies WHERE title=?', (defaults['title'],))
    
    # Remove any movies with zero or negative ratings
    cursor.execute('DELETE FROM movies WHERE rating <= 0')
    
    # Remove any movies with invalid years (0 or future years)
    current_year = 2025  # You can update this as needed
    cursor.execute('DELETE FROM movies WHERE year <= 0 OR year > ?', (current_year,))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

def print_database_stats():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    # Count total movies
    cursor.execute('SELECT COUNT(*) FROM movies')
    total_movies = cursor.fetchone()[0]
    
    # Count movies by genre
    cursor.execute('SELECT genre, COUNT(*) FROM movies GROUP BY genre')
    genre_counts = cursor.fetchall()
    
    # Get rating statistics
    cursor.execute('SELECT AVG(rating), MIN(rating), MAX(rating) FROM movies')
    rating_stats = cursor.fetchone()
    
    # Get year range
    cursor.execute('SELECT MIN(year), MAX(year) FROM movies')
    year_range = cursor.fetchone()
    
    print("\nDatabase Statistics:")
    print(f"Total movies: {total_movies}")
    print("\nMovies by genre:")
    for genre, count in genre_counts:
        print(f"  {genre}: {count}")
    print("\nRating statistics:")
    print(f"  Average: {rating_stats[0]:.2f}")
    print(f"  Range: {rating_stats[1]} - {rating_stats[2]}")
    print("\nYear range:")
    print(f"  {year_range[0]} - {year_range[1]}")
    
    conn.close()

if __name__ == "__main__":
    print("Cleaning database...")
    clean_database()
    print("Database cleaned successfully!")
    print_database_stats()
