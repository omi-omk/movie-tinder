class Movie:
    def __init__(self, id, title, genre, description):
        self.id = id
        self.title = title
        self.genre = genre
        self.description = description

    def __repr__(self):
        return f"Movie(id={self.id}, title='{self.title}', genre='{self.genre}', description='{self.description}')"
