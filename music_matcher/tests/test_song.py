import pytest

from music_matcher.song import Song, SongError, SongTypeError


@pytest.mark.parametrize('title,genre,artist,year', [
    ('Invierno Nuclear', 'electronic', 'VVV[Trippin\' you', 2020),
    ('Nadie es Leal', 'electronic', 'VVV[Trippin\' you', 2021)
])
def test_song_init(title: str, genre: str, artist: str, year: int):
    Song(title=title, genre=genre, artist=artist, year=year)


@pytest.mark.parametrize('title,genre,artist,year,expected_exception', [
    (3, 'rock', 'VVV[Trippin\' you', 1998, SongTypeError),
    ('Hiedra Verde', None, 'VVV[Trippin\' you', 2021, SongTypeError),
    ('Fuego Cruzado', 'electronic', None, 2021, SongTypeError),
    ('Odiar Frontal', 'electronic', 'VVV[Trippin\' you', None, SongTypeError),
    ('Monstruo', 'electronic', 'VVV[Trippin\' you', -92, SongError),
])
def test_song_init_ko(title: str, genre: str, artist: str, year: int,
                      expected_exception: Exception):
    with pytest.raises(expected_exception):
        Song(title=title, genre=genre, artist=artist, year=year)
