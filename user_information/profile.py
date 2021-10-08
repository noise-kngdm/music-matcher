class Profile:
    '''A class representing an user of the application'''
    def __init__(self, age, name, gender, favourite_music_genre, favourite_artists, music_history):
        self.age = age
        self.name = name
        self.gender = gender
        self.favourite_music_genre = favourite_music_genre
        self.favourite_artists = favourite_artists
        self.music_history = music_history