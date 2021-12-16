'''Tests for the user.py file.'''

import pytest
from assertpy import assert_that

from music_matcher.user import User, UserError, UserTypeError
from music_matcher.music_history import MusicHistory


@pytest.mark.parametrize('birthdate', ['2001-01-01'])
@pytest.mark.parametrize('name, username', [
    ('Lucia Manson', 'lucia_manson_666'),
    ('Luis Javier', 'luisiyo')
])
@pytest.mark.parametrize('gender', ['W', 'M', 'O', 'NB'])
def test_user_init(lucia_music_history: MusicHistory, gender: str,
                   name: str, username: str, birthdate: str):
    """Test that User's constructor is working.

    Parameters
    ----------
    lucia_music_history : MusicHistory
        MusicHistory of the user.
    gender : str
        Gender of the user.
    name : str
        Name of the user.
    username : str
        Username of the user.
    birthdate : str
        Birthdate of the user in the YYYY-MM-DD format.
    """
    user = User(username=username, name=name, gender=gender,
                birthdate=birthdate, music_history=lucia_music_history)
    assert_that(user).is_type_of(User)


@pytest.mark.parametrize('gender,name,username,birthdate,expected_exception', [
    ('M', 'Luis', 3, '2021-01-01', UserTypeError),
    ('M', 'Luis', 'luisiyo', None, UserTypeError),
    (3, 'Luis', 'luisiyo', '2021-01-01', UserTypeError),
    ('a', 'Luis', 'luisiyo', '2021-01-01', UserError),
    ])
def test_user_init_ko(lucia_music_history: MusicHistory, gender: str,
                      name: str, username: str, birthdate: str,
                      expected_exception: Exception):
    """Test that User's constructor is raising exception when called with wrong parameters.

    Parameters
    ----------
    lucia_music_history : MusicHistory
        MusicHistory of the user.
    gender : str
        Gender of the user.
    name : str
        Name of the user.
    username : str
        Username of the user.
    birthdate : str
        Birthdate of the user in the YYYY-MM-DD format.
    expected_exception : Exception
        Exception that should be raised.
    """
    with pytest.raises(expected_exception):
        User(username=username, name=name, gender=gender,
             birthdate=birthdate, music_history=lucia_music_history)


def test_user_init_ko_music_history():
    """Test that User's constructor is raising exception when called with a wrong MusicHistory.."""
    with pytest.raises(UserTypeError):
        User(username='davii', name='David', gender='M',
             birthdate='2000-12-02', music_history=None)
