from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import Database
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
db = Database()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        user_id = db.get_user_id(username)
        if not user_id:
            user_id = db.add_user(username)
        session['user_id'] = user_id
        session['username'] = username
        session['movies_shown'] = 0
        
        # Get all available movies
        all_movies = db.get_movies()
        if not all_movies:
            return render_template('index.html', error="No movies available in the database. Please try again later.")
        
        # Select min(10, available_movies) random movies
        num_movies = min(10, len(all_movies))
        selected_movies = random.sample(all_movies, num_movies)
        session['selected_movies'] = selected_movies
        session['total_movies'] = num_movies
        
        return redirect(url_for('swipe'))
    return render_template('index.html')

@app.route('/swipe', methods=['GET', 'POST'])
def swipe():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        action = request.form['action']
        db.record_swipe(session['user_id'], movie_id, action)
        session['movies_shown'] += 1
        
        if session['movies_shown'] >= session['total_movies']:
            return redirect(url_for('recommendations'))
        return redirect(url_for('swipe'))
    
    if session['movies_shown'] >= session['total_movies']:
        return redirect(url_for('recommendations'))
    
    current_movie = session['selected_movies'][session['movies_shown']]
    return render_template('swipe.html', 
                         movie=current_movie, 
                         username=session['username'],
                         progress=session['movies_shown'] + 1,
                         total=session['total_movies'])

@app.route('/recommendations')
def recommendations():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    recommended_movies = db.get_recommendations(session['user_id'])
    print(f"Found {len(recommended_movies)} recommended movies for user {session['user_id']}")
    
    # If no recommendations, get top rated unseen and uninteracted movies
    if not recommended_movies:
        print("No recommendations found, getting top rated unseen movies instead")
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM movies 
            WHERE id NOT IN (
                SELECT movie_id FROM swipes
                WHERE user_id = ?
                AND action !='not_seen'
            )
            ORDER BY rating DESC LIMIT 5
        ''', (session['user_id'],))
        recommended_movies = cursor.fetchall()
        conn.close()
    
    # If still no recommendations, show a message
    if not recommended_movies:
        return render_template('no_recommendations.html',
                           username=session['username'])
    
    return render_template('recommendations.html', 
                         movies=recommended_movies,
                         username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)
