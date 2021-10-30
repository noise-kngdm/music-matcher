"""
A module that represents all information related to music metadata.
"""
class Song:
    '''A class representing the information of a song. '''
    def __init__(self, title: str, music_genre: str, artist: str, year: int):
        '''
        Song class constructor.

        Attributes
        ----------
        title : str
            It's the title of the song.
        music_genre : str
            The song's music genre.
        artist : str
            The singer or band who composed the song.
        year : int
            The year when the song was released.
        '''
        self.title = title
        self.music_genre = music_genre
        self.artist = artist
        self.year = year
