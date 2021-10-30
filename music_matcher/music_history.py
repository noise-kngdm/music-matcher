"""Module that represents a user profile."""
from typing import List
from datetime import datetime
from music_matcher.song import Song


class SongEntry:
    '''Song with metadata to save into a user music history.'''
    def __init__(self, song: Song, times_played: List[datetime]):
        '''
        SongEntry constructor.

        Attributesu
        ----------
        song : Song
            Song played.
        times_played : List[datetime]
            Dates when the song was played.
        '''
        self.song = song
        self.times_played = times_played


class MusicHistory:
    '''A class representing the music history of an user.'''
    def __init__(self,songs_played: List[SongEntry]):
        '''
        MusicHistory class constructor.

            Attributes
            ----------
            songs_played : list of SongEntry
                    List of all songs played by an user.
        '''
        self.songs_played = songs_played
