"""Module that represents a user profile."""
from datetime import datetime
from music_matcher.music_history import MusicHistory


class User:
    '''A user of the application.'''
    def __init__(self, birth_date: datetime, name: str, gender: str, music_history: MusicHistory):
        '''
        User class constructor.

            Attributes
            ----------
            birth_date : datetime
                User's birth date.
            name : str
                User's name.
            gender : str
                User's gender.
            music_history : MusicHistory
                User's music history.
        '''
        self.birth_date = birth_date
        self.name = name
        self.gender = gender
        self.music_history = music_history
