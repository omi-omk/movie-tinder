import os
import sqlite3
from database import Database

def init_database():
    # Delete existing database file if it exists
    if os.path.exists('movies.db'):
        os.remove('movies.db')
    
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Drop existing tables
    cursor.execute('DROP TABLE IF EXISTS movies')
    
    # Create table with updated schema
    cursor.execute('''CREATE TABLE movies
                     (id INTEGER PRIMARY KEY,
                      title TEXT,
                      genre TEXT,
                      description TEXT,
                      rating FLOAT,
                      year INTEGER,
                      director TEXT,
                      actors TEXT,
                      keywords TEXT,
                      poster TEXT)''')

    # Sample movies with ratings and years
    movies = [
        (1, "The Shawshank Redemption", "Drama", "Two imprisoned men bond over a number of years.", 9.3, 1994, "Frank Darabont", "Tim Robbins, Morgan Freeman", "prison, hope", "shawshank_redemption.jpg"),
        (2, "The Godfather", "Crime/Drama", "The aging patriarch of an organized crime dynasty transfers control to his son.", 9.2, 1972, "Francis Ford Coppola", "Marlon Brando, Al Pacino", "mafia, family", "godfather.jpg"),
        (3, "The Dark Knight", "Action/Crime/Drama", "Batman confronts the mysterious Joker who wreaks havoc on Gotham City.", 9.0, 2008, "Christopher Nolan", "Christian Bale, Heath Ledger", "superhero, batman", "dark_knight.jpg"),
        (4, "Pulp Fiction", "Crime/Drama", "Various interconnected stories of criminal Los Angeles.", 8.9, 1994, "Quentin Tarantino", "John Travolta, Samuel L. Jackson", "crime, violence", "pulp_fiction.jpg"),
        (5, "Inception", "Action/Sci-Fi", "A thief who enters the dreams of others to steal secrets.", 8.8, 2010, "Christopher Nolan", "Leonardo DiCaprio, Joseph Gordon-Levitt", "dreams, sci-fi", "inception.jpg"),
        (6, "The Matrix", "Action/Sci-Fi", "A computer programmer discovers a mysterious world of digital reality.", 8.7, 1999, "The Wachowskis", "Keanu Reeves, Laurence Fishburne", "sci-fi, matrix", "matrix.jpg"),
        (7, "Forrest Gump", "Drama/Romance", "The life journey of a man with a low IQ but great heart.", 8.8, 1994, "Robert Zemeckis", "Tom Hanks, Robin Wright", "drama, romance", "forrest_gump.jpg"),
        (8, "Fight Club", "Drama", "An insomniac office worker forms an underground fight club.", 8.8, 1999, "David Fincher", "Brad Pitt, Edward Norton", "drama, fight", "fight_club.jpg"),
        (9, "The Lord of the Rings: The Fellowship of the Ring", "Action/Adventure/Fantasy", "A hobbit begins a journey to destroy a powerful ring.", 8.8, 2001, "Peter Jackson", "Elijah Wood, Viggo Mortensen", "fantasy, adventure", "lord_of_the_rings.jpg"),
        (10, "Goodfellas", "Biography/Crime/Drama", "The story of Henry Hill and his life in the mob.", 8.7, 1990, "Martin Scorsese", "Robert De Niro, Joe Pesci", "crime, biography", "goodfellas.jpg"),
        (11, "The Silence of the Lambs", "Crime/Drama/Thriller", "An FBI cadet must receive the help of an incarcerated cannibal killer.", 8.6, 1991, "Jonathan Demme", "Jodie Foster, Anthony Hopkins", "thriller, crime", "silence_of_the_lambs.jpg"),
        (12, "Interstellar", "Adventure/Drama/Sci-Fi", "Explorers travel through a wormhole in search of a new home for humanity.", 8.6, 2014, "Christopher Nolan", "Matthew McConaughey, Anne Hathaway", "sci-fi, adventure", "interstellar.jpg"),
        (13, "The Green Mile", "Crime/Drama/Fantasy", "The lives of guards on Death Row are affected by one of their charges.", 8.6, 1999, "Frank Darabont", "Tom Hanks, Michael Clarke Duncan", "fantasy, drama", "green_mile.jpg"),
        (14, "Saving Private Ryan", "Drama/War", "Following the Normandy Landings, a group of soldiers go behind enemy lines.", 8.6, 1998, "Steven Spielberg", "Tom Hanks, Matt Damon", "war, drama", "saving_private_ryan.jpg"),
        (15, "Jurassic Park", "Action/Adventure/Sci-Fi", "A theme park suffers a major power breakdown that allows its cloned dinosaurs to run amok.", 8.1, 1993, "Steven Spielberg", "Sam Neill, Laura Dern", "sci-fi, adventure", "jurassic_park.jpg"),
        (16, "The Avengers", "Action/Adventure/Sci-Fi", "Earth's mightiest heroes must come together to save the world.", 8.0, 2012, "Joss Whedon", "Robert Downey Jr., Chris Evans", "superhero, sci-fi", "avengers.jpg"),
        (17, "Back to the Future", "Adventure/Comedy/Sci-Fi", "A teenager is accidentally sent 30 years into the past in a time-traveling car.", 8.5, 1985, "Robert Zemeckis", "Michael J. Fox, Christopher Lloyd", "sci-fi, comedy", "back_to_the_future.jpg"),
        (18, "Gladiator", "Action/Adventure/Drama", "A former Roman General seeks justice after being betrayed.", 8.5, 2000, "Ridley Scott", "Russell Crowe, Joaquin Phoenix", "action, drama", "gladiator.jpg"),
        (19, "The Departed", "Crime/Drama/Thriller", "An undercover cop and a mole in the police attempt to identify each other.", 8.5, 2006, "Martin Scorsese", "Leonardo DiCaprio, Matt Damon", "crime, thriller", "departed.jpg"),
        (20, "The Lion King", "Animation/Adventure/Drama", "A young lion prince flees his kingdom after the murder of his father.", 8.5, 1994, "Roger Allers, Rob Minkoff", "James Earl Jones, Matthew Broderick", "animation, adventure", "lion_king.jpg"),
        (21, "Whiplash", "Drama/Music", "A promising young drummer enrolls at a cut-throat music conservatory.", 8.5, 2014, "Damien Chazelle", "Miles Teller, J.K. Simmons", "drama, music", "whiplash.jpg"),
        (22, "The Prestige", "Drama/Mystery/Sci-Fi", "Two stage magicians engage in competitive one-upmanship.", 8.5, 2006, "Christopher Nolan", "Hugh Jackman, Christian Bale", "mystery, sci-fi", "prestige.jpg"),
        (23, "Eternal Sunshine of the Spotless Mind", "Drama/Romance/Sci-Fi", "A couple undergoes a medical procedure to erase each other from their memories.", 8.3, 2004, "Michel Gondry", "Jim Carrey, Kate Winslet", "romance, sci-fi", "eternal_sunshine.jpg"),
        (24, "Memento", "Mystery/Thriller", "A man with short-term memory loss attempts to track down his wife's murderer.", 8.4, 2000, "Christopher Nolan", "Guy Pearce, Carrie-Anne Moss", "mystery, thriller", "memento.jpg"),
        (25, "The Social Network", "Biography/Drama", "The founding of Facebook and the resulting lawsuits.", 7.7, 2010, "David Fincher", "Jesse Eisenberg, Andrew Garfield", "biography, drama", "social_network.jpg"),
        (26, "La La Land", "Comedy/Drama/Music", "A jazz pianist and an aspiring actress fall in love while pursuing their dreams.", 8.0, 2016, "Damien Chazelle", "Ryan Gosling, Emma Stone", "comedy, romance", "la_la_land.jpg"),
        (27, "The Grand Budapest Hotel", "Adventure/Comedy/Crime", "A concierge and his lobby boy become embroiled in theft and murder.", 8.1, 2014, "Wes Anderson", "Ralph Fiennes, Tony Revolori", "comedy, adventure", "grand_budapest_hotel.jpg"),
        (28, "Mad Max: Fury Road", "Action/Adventure/Sci-Fi", "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler.", 8.1, 2015, "George Miller", "Tom Hardy, Charlize Theron", "action, sci-fi", "mad_max.jpg"),
        (29, "The Big Lebowski", "Comedy/Crime", "A laid-back bowling enthusiast gets caught up in a series of misadventures.", 8.1, 1998, "Joel Coen, Ethan Coen", "Jeff Bridges, John Goodman", "comedy, crime", "big_lebowski.jpg"),
        (30, "Blade Runner 2049", "Action/Drama/Sci-Fi", "A blade runner discovers a long-buried secret that leads to a quest.", 8.0, 2017, "Denis Villeneuve", "Ryan Gosling, Harrison Ford", "sci-fi, action", "blade_runner.jpg"),
        (31, "Get Out", "Horror/Mystery/Thriller", "A young African-American visits his white girlfriend's parents for the weekend.", 7.7, 2017, "Jordan Peele", "Daniel Kaluuya, Allison Williams", "horror, mystery", "get_out.jpg"),
        (32, "The Shape of Water", "Drama/Fantasy/Romance", "A janitor forms a relationship with an amphibious creature.", 7.3, 2017, "Guillermo del Toro", "Sally Hawkins, Michael Shannon", "fantasy, romance", "shape_of_water.jpg"),
        (33, "Black Panther", "Action/Adventure", "T'Challa, heir to Wakanda, must step forward to lead his people.", 7.3, 2018, "Ryan Coogler", "Chadwick Boseman, Michael B. Jordan", "action, adventure", "black_panther.jpg"),
        (34, "Parasite", "Comedy/Drama/Thriller", "A poor family schemes to become employed by a wealthy family.", 8.6, 2019, "Bong Joon-ho", "Song Kang-ho, Lee Sun-kyun", "comedy, drama", "parasite.jpg"),
        (35, "Joker", "Crime/Drama/Thriller", "A failed comedian turns to a life of crime in Gotham City.", 8.4, 2019, "Todd Phillips", "Joaquin Phoenix, Robert De Niro", "crime, drama", "joker.jpg"),
        (36, "1917", "Drama/War", "Two soldiers must deliver a message that will stop 1,600 men from walking into a trap.", 8.3, 2019, "Sam Mendes", "George MacKay, Dean-Charles Chapman", "war, drama", "1917.jpg"),
        (37, "The Irishman", "Biography/Crime/Drama", "A truck driver becomes a hitman involved with a crime family.", 7.8, 2019, "Martin Scorsese", "Robert De Niro, Al Pacino", "biography, crime", "irishman.jpg"),
        (38, "Once Upon a Time in Hollywood", "Comedy/Drama", "A faded TV actor and his stunt double strive to achieve fame in Hollywood.", 7.6, 2019, "Quentin Tarantino", "Leonardo DiCaprio, Brad Pitt", "comedy, drama", "once_upon_a_time.jpg"),
        (39, "Dune", "Action/Adventure/Drama", "A noble family becomes embroiled in a war for control over a desert planet.", 8.0, 2021, "Denis Villeneuve", "Timothée Chalamet, Rebecca Ferguson", "action, adventure", "dune.jpg"),
        (40, "No Time to Die", "Action/Adventure/Thriller", "James Bond has left active service but is drawn back into action.", 7.3, 2021, "Cary Joji Fukunaga", "Daniel Craig, Léa Seydoux", "action, adventure", "no_time_to_die.jpg"),
        (41, "The French Dispatch", "Comedy/Drama/Romance", "A love letter to journalists set in an outpost of an American newspaper.", 7.2, 2021, "Wes Anderson", "Benicio del Toro, Adrien Brody", "comedy, romance", "french_dispatch.jpg"),
        (42, "Spider-Man: No Way Home", "Action/Adventure/Fantasy", "Spider-Man seeks help from Doctor Strange to make his identity secret.", 8.2, 2021, "Jon Watts", "Tom Holland, Zendaya", "superhero, fantasy", "spider_man.jpg"),
        (43, "The Batman", "Action/Crime/Drama", "Batman investigates corruption in Gotham and confronts the Riddler.", 7.8, 2022, "Matt Reeves", "Robert Pattinson, Zoë Kravitz", "action, crime", "batman.jpg"),
        (44, "Top Gun: Maverick", "Action/Drama", "After thirty years, Maverick is still pushing the envelope as a top naval aviator.", 8.3, 2022, "Joseph Kosinski", "Tom Cruise, Miles Teller", "action, drama", "top_gun.jpg"),
        (45, "Everything Everywhere All at Once", "Action/Adventure/Comedy", "An aging Chinese immigrant is swept up in an insane adventure.", 7.9, 2022, "Daniel Kwan, Daniel Scheinert", "Michelle Yeoh, Ke Huy Quan", "action, comedy", "everything_everywhere.jpg"),
        (46, "Avatar: The Way of Water", "Action/Adventure/Fantasy", "Jake Sully lives with his newfound family formed on the planet of Pandora.", 7.6, 2022, "James Cameron", "Sam Worthington, Zoe Saldana", "action, fantasy", "avatar.jpg"),
        (47, "The Whale", "Drama", "A reclusive English teacher attempts to reconnect with his estranged teenage daughter.", 7.7, 2022, "Darren Aronofsky", "Brendan Fraser, Sadie Sink", "drama", "whale.jpg"),
        (48, "Oppenheimer", "Biography/Drama/History", "The story of American scientist J. Robert Oppenheimer and the atomic bomb.", 8.5, 2023, "Christopher Nolan", "Cillian Murphy, Emily Blunt", "biography, drama", "oppenheimer.jpg"),
        (49, "Barbie", "Adventure/Comedy/Fantasy", "Barbie and Ken go on a journey of self-discovery in the real world.", 7.0, 2023, "Greta Gerwig", "Margot Robbie, Ryan Gosling", "adventure, comedy", "barbie.jpg"),
        (50, "Mission: Impossible - Dead Reckoning Part One", "Action/Adventure/Thriller", "Ethan Hunt and his IMF team must track down a dangerous weapon.", 7.8, 2023, "Christopher McQuarrie", "Tom Cruise, Hayley Atwell", "action, adventure", "mission_impossible.jpg"),
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO movies (id, title, genre, description, rating, year, director, actors, keywords, poster) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', movies)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized with 50 sample movies!")
