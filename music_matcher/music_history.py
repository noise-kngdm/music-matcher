"""Module that represents a user profile."""
from datetime import datetime
from dataclasses import dataclass

from music_matcher.song import Song


class SongEntryTypeError(TypeError):
    '''Exception that will be raised when a SongEntry method
       is called using a parameter with a wrong type.'''


@dataclass
class SongEntry:
    '''Song with metadata to save into a user music history.'''
    song: Song
    times_played: list[datetime]

    def __post_init__(self):
        """Part of the constructor not initialized by the
           dataclass construction.

        Raises
        ------
        SongEntryTypeError
            If any of the parameters has  an incorrect type.
        """
        if not isinstance(self.song, Song):
            raise SongEntryTypeError('The type of song must be Song and '
                                     f'not {type(self.song)}')
        if not isinstance(self.times_played, list):
            raise SongEntryTypeError('The type of times_played must be list'
                                     f' of datetime and not {type(self.times_played)}')
        for timestamp in self.times_played:
            if not isinstance(timestamp, datetime):
                raise SongEntryTypeError('The type of every item in times_played must be'
                                         f' datetime and not {type(timestamp)}')

    @property
    def genre(self):
        '''
        Return the music genre of the song.

        Returns
        -------
        str
            The music genre of the song.
        '''
        return self.song.genre

    @property
    def amount_reproductions(self) -> int:
        '''
        Return the amount of times the song was played.

        Returns
        -------
        int
            Amount of times the song was played.
        '''
        return len(self.times_played)


class MusicHistoryTypeError(Exception):
    '''Exception that will be raised when a MusicHistory method
       is called using a parameter with a wrong type.'''


class MusicHistory:
    '''A class representing the music history of an user.'''
    def __init__(self, songs_played: list[SongEntry]):
        '''
        MusicHistory class constructor.

            Attributes
            ----------
            songs_played : list of SongEntry
                    List of all songs played by an user.
        '''
        if not isinstance(songs_played, list):
            raise MusicHistoryTypeError(
                'The type of songs_played must be list of SongEntry'
                f' and not {type(songs_played)}')

        for song in songs_played:
            if not isinstance(song, SongEntry):
                raise MusicHistoryTypeError(
                    'The type of every songs_played item must be SongEntry'
                    f' and not {type(song)}')

        self._songs_played = songs_played

    def __len__(self) -> int:
        return len(self._songs_played)

    def __repr__(self) -> str:
        return self._songs_played.__repr__()

    @property
    def genres_listened(self) -> set[str]:
        '''
        Return a set with all the music genres included in
        the music history.

        Returns
        -------
        set[str]
            Set with all the music genres listened by the user.
        '''
        return {x.genre for x in self._songs_played}

    @property
    def total_entries(self) -> int:
        '''
        Return total amount of songs played by the user.

        Returns
        -------
        int
            Total amount of songs played by the user.
        '''
        return sum([len(x.times_played) for x in self._songs_played])

    @property
    def genre_preferences(self) -> dict[str:float]:
        """
        Return a dictionary containing information about the music genres
        listened the most by the user.

        Returns
        -------
        dict[str:float]
            A dictionary where the key is the name of the music genre
            and the value a number representing the percentage of listening
            time that the user spent listening to that genre.
        """
        total_entries = self.total_entries
        preferences = {k: 0 for k in self.genres_listened}
        return dict(map(lambda x: (x[0], sum(
            [song.amount_reproductions for song in self._songs_played
             if song.genre == x[0]
             ])/total_entries), preferences.items())
            )
