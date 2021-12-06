"""Module that represents a user profile."""
from datetime import datetime
from dataclasses import dataclass

from music_matcher.song import Song


@dataclass
class SongEntry:
    '''Song with metadata to save into a user music history.'''
    song: Song
    times_played: list[datetime]

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
    def number_times_played(self) -> int:
        '''
        Return the amount of times the song was played.

        Returns
        -------
        int
            Amount of times the song was played.
        '''
        return len(self.times_played)


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
        self._songs_played = songs_played

    def __len__(self) -> int:
        return len(self._songs_played)

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
        return {x for x in self._songs_played.genre}

    @property
    def total_entries(self) -> int:
        '''
        Return total amount of songs played by the user.

        Returns
        -------
        int
            Total amount of songs played by the user.
        '''
        return sum([x.times_played for x in self._songs_played])

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
        total_entries = self._music_history.total_entries
        preferences = {k: 0 for k in self._music_history.genres_listened()}
        return dict(map(lambda x: (x[0], sum(
            [song.times_played for song in self._songs_played
             if song.genre == x[0]
             ])/total_entries), preferences.items())
            )
