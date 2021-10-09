class MusicHistory:
    '''A class representing the music history of an user'''
    def __init__(self,songs_played, music_genres_played, favourite_songs, playlists):
        ''' MusicHistory class constructor
            
            Attributes
            ----------
            songs_played : list of Song objects
                    List of all songs played by an user.
            music_genres_played : list of string
                    List of all music genres played by an user.
            favourite_songs : list of Song objects 
                    List of user's favourite songs.
            playlists : list with lists of Songs objects.
                    All the playlists created by the user.
        '''
        self.songs_played = songs_played
        self.music_genres_played = music_genres_played
        self.favourite_songs = favourite_songs
        self.playlists = playlists
