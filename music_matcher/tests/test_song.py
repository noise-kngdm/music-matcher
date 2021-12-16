'''Tests for the song.py file.'''

import pytest
from assertpy import assert_that

from music_matcher.song import Song, SongError, SongTypeError


@pytest.mark.parametrize('title,genre,artist,year', [
    ('Invierno Nuclear', 'electronic', 'VVV[Trippin\' you', 2020),
    ('Nadie es Leal', 'electronic', 'VVV[Trippin\' you', 2021)
])
def test_song_init(title: str, genre: str, artist: str, year: int):
    """Test that Song's constructor is working.

    Parameters
    ----------
    title : str
        Title of the song.
    genre : str
        Music genre of the song.
    artist : str
        Artist of the song.
    year : int
        Year when the song was first published.
    """
    song = Song(title=title, genre=genre, artist=artist, year=year)
    assert_that(song).is_type_of(Song)


@pytest.mark.parametrize('title,genre,artist,year,expected_exception', [
    (3, 'rock', 'VVV[Trippin\' you', 1998, SongTypeError),
    ('Hiedra Verde', None, 'VVV[Trippin\' you', 2021, SongTypeError),
    ('Fuego Cruzado', 'electronic', None, 2021, SongTypeError),
    ('Odiar Frontal', 'electronic', 'VVV[Trippin\' you', None, SongTypeError),
    ('Monstruo', 'electronic', 'VVV[Trippin\' you', -92, SongError),
])
def test_song_init_ko(title: str, genre: str, artist: str, year: int,
                      expected_exception: Exception):
    """Test that Song's constructor is raising exception when called with wrong parameters.

    Parameters
    ----------
    title : str
        Title of the song.
    genre : str
        Music genre of the song.
    artist : str
        Artist of the song.
    year : int
        Year when the song was first published.
    expected_exception : Exception
        Exception that should have been raised.
"""
    with pytest.raises(expected_exception):
        Song(title=title, genre=genre, artist=artist, year=year)
