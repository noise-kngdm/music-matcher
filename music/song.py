class Song:
    '''A class representing the information of a song'''
    def __init__(self, title, music_genre, song_length, artist, related_songs):
        self.title = title
        self.music_genre = music_genre
        self.song_length = song_length
        self.author = artist
        self.related_songs = related_songs