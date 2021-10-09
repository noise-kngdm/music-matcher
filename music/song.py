class Song:
    '''A class representing the information of a song '''
    def __init__(self, title, music_genre, song_length, artist, related_songs):
        ''' Song class constructor
            
            Attributes
            ----------
            title : string
                    It's the title of the song.
            music_genre : string
                    Music genre which it belongs.
            song_length : float 
                    The time it takes to play.
            artist : string
                    The singer or band who composed the song.
            related_songs: list of string
                    List of similar songs.
        '''
        self.title = title
        self.music_genre = music_genre
        self.song_length = song_length
        self.artist = artist
        self.related_songs = related_songs
