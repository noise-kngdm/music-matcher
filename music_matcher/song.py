"""
A module that represents all information related to music metadata.
"""

from dataclasses import dataclass


class SongError(ValueError):
    pass


class SongTypeError(ValueError):
    pass


@dataclass
class Song:
    '''A class representing the information of a song.

       Attributes
       ----------
       title : str
           It's the title of the song.
       genre : str
           The song's music genre. It should be a string with genres separated
           by a ';' symbol.
       artist : str
           The singer or band who composed the song.
       year : int
           The year when the song was released.
    '''
    title: str
    genre: str
    artist: str
    year: int

    def __post_init__(self):
        """Part of the constructor not initialized by the
           dataclass construction.

        """
        if not isinstance(self.title, str):
            raise SongTypeError('The title must be of str type.')

        if not isinstance(self.genre, str):
            raise SongTypeError('The genre must be of str type.')

        if not isinstance(self.artist, str):
            raise SongTypeError('The artist must be of str type.')

        if not isinstance(self.year, int):
            raise SongTypeError('The year must be of int type.')
        if self.year < 0:
            raise SongError('The year attribute must be a valid year.')
