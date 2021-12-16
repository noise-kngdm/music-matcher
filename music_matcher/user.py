"""Module that represents a user profile."""
from datetime import datetime
from dataclasses import dataclass

from music_matcher.music_history import MusicHistory


class UserError(ValueError):
    '''Exception that will be raised when the User class
       has encountered a wrong value in the parameters of a method.'''


class UserTypeError(ValueError):
    '''Exception that will be raised when a User method
       is called using a parameter with a wrong type.'''


@dataclass(order=True)
class User:
    '''A user of the application.

        Attributes
        ----------
        username : str
            Unique username.
        birth_date : datetime
            User's birth date.
        name : str
            User's name.
        gender : str
            User's gender.
        music_history : MusicHistory
            User's music history.
    '''
    username: str
    birthdate: datetime
    name: str
    gender: str
    music_history: MusicHistory

    VALID_GENRES = ['W', 'M', 'O', 'NB']

    def __post_init__(self):
        """Part of the constructor not initialized by the
           dataclass construction.

        Raises
        ------
        UserTypeError
            If any of the parameters has  an incorrect type.
        UserError
            If the birthdate or gender parameters doesn't have
            the expected format.
        """

        if not isinstance(self.birthdate, str):
            raise UserTypeError('The birthdate must be of str type')
        try:
            self.birthdate = datetime.fromisoformat(self.birthdate)
        except TypeError as error:
            raise UserError('The birthdate must be in <YYYY-MM-DD> format') from error

        try:
            self.gender = self.gender.upper()
        except AttributeError as error:
            raise UserTypeError('The gender must be of str type') from error
        if self.gender not in User.VALID_GENRES:
            raise UserError('The gender introduced must be one'
                            f' of the following:{User.VALID_GENRES}')

        if not isinstance(self.name, str):
            raise UserTypeError('The name must be of str type.')

        if not isinstance(self.username, str):
            raise UserTypeError('The username must be of str type')

        if not isinstance(self.music_history, MusicHistory):
            raise UserTypeError('The music_history must be of'
                                ' MusicHistory type')
