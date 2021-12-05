"""Module that represents a user profile."""
from datetime import datetime
from music_matcher.music_history import MusicHistory


class User:
    '''A user of the application.'''
    def __init__(self, birth_date: datetime, name: str, gender: str,
                 music_history: MusicHistory, username: str):
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
            username : str
                Unique username.
        '''
        self._birth_date = birth_date
        self._name = name
        self._gender = gender
        self._music_history = music_history
        self._username = username

    def __lt__(self, other):
        return self.username < other.username

    @property
    def music_history(self) -> MusicHistory:
        """
        Return the music history of the user.

        Returns
        -------
        MusicHistory
            The music history of the user
        """
        return self._music_history
