class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.swipes = []

    def swipe(self, movie_id, action):
        self.swipes.append((movie_id, action))

    def get_recommendations(self):
        # Logic to recommend movies based on swipes
        pass
