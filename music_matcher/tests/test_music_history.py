'''Tests for the music_history.py file.'''

from datetime import timedelta, datetime

import pytest
from assertpy import assert_that

import music_matcher.music_history as mh
from music_matcher.song import Song
from .conftest import genres, valid_date


LENGTH_GENRES = len(genres())


@pytest.fixture(params=[(genres(), i) for i in range(LENGTH_GENRES)])
def get_song(songs, request) -> Song:
    """
    Return a song from the songs() fixture.

    Parameters
    ----------
    songs : fixture
        Song's factory as fixture.
    request : SubRequest:
        Fixture construction used to obtain the fixture's params.
    request.param : list[tuple[str,int]]
        List composed of tuples of str and int, being the string the name of the music
        genre and the int the number of songs (up to 10) that will be added from that
        music genre to the MusicHistory object returned.

    Returns
    -------
    Song
        The requested Song instance.
    """
    genres = request.param[0]
    index = request.param[1]
    return songs([(genres[index], 1), ])[0]


def test_song_entry_init(get_song):
    """Test that SongEntry's constructor is working.

    Parameters
    ----------
    get_song : fixture
        Fixture that return a song instance.
    """
    song_entry = mh.SongEntry(get_song, [valid_date()])
    assert_that(song_entry).is_type_of(mh.SongEntry)


def valid_song() -> Song:
    """Return an initialized song.

    Returns
    -------
    Song
        Valid song.
    """
    return Song('Lake Fantasy', 'blackgaze', 'Lantlôs', 2021)


@pytest.mark.parametrize('song, times_played', [
    (None, None),
    (valid_song(), [False]),
    (valid_song(), [valid_date(), 1]),
    (None, [valid_date()])
])
def test_song_entry_init_ko(song: Song, times_played: datetime):
    '''
    Test that SongEntry's constructor is raising exception when called with wrong parameters.

    Parameters
    ----------
    song : Song
        Song that will be used to initialize the SongEntry instance.
    times_played : datetime
        Timestamp that will be used to initialize the song.
    '''
    with pytest.raises(mh.SongEntryTypeError):
        mh.SongEntry(song, times_played)


def test_song_entry_genre(get_song):
    """
    Test the SongEntry's genre method.

    Parameters
    ----------
    get_song : fixture
        Fixture that returns a song instance.
    """
    song_entry = mh.SongEntry(get_song, [valid_date()])
    assert_that(song_entry.genre).is_equal_to(get_song.genre)


@pytest.fixture(params=[0, 3, 7])
def times_played(request):
    """
    Fixture that returns a list of days.

    The days will be a list of dates starting from the date returned by the valid_date()
    fixture, having each entry list a number of days substracted from that original date
    being this number from 0 to the one specified in the fixture parameter.

    Parameters
    ----------
    request : SubRequest:
        Fixture construction used to obtain the fixture's params.
    request.param : int
        Number of days that will be returned.

    Returns
    -------
    list[datetime]
        List of days.
    """
    return [valid_date() - timedelta(days=i) for i in range(request.param)]


def test_song_entry_amount_reproductions(get_song, times_played):
    """
    Test the SongEntry's amount_reproductions method.

    Parameters
    ----------
    get_song : fixture
        Fixture that returns a song.
    times_played : fixture
        Fixture that returns a list of dates.
    """
    song_entry = mh.SongEntry(get_song, times_played)
    assert_that(song_entry.amount_reproductions).is_equal_to(len(times_played))


@pytest.mark.parametrize('songs_param', [[('metal', 10)]])
def test_music_history_init(songs, times_played, songs_param: list[tuple[str, int]]):
    """Test that MusicHistory's constructor is working.

    Parameters
    ----------
    songs : fixture
        Fixture that returns a list of songs.
    times_played : fixture
        Fixture that returns a list of dates.
    songs_param : list[tuple[str,int]]
        List composed of tuples of str and int, being the string the name of the music
        genre and the int the number of songs (up to 10) that will be added from that
        music genre to the MusicHistory object returned.
    """
    song_entries = [mh.SongEntry(song, times_played) for song in songs(songs_param)]
    music_history = mh.MusicHistory(song_entries)
    assert_that(music_history).is_type_of(mh.MusicHistory)


@pytest.mark.parametrize('song_entries', [
    None,
    [False],
    [mh.SongEntry(valid_song(), [valid_date()]), False],
])
def test_music_history_init_ko(song_entries):
    '''
    Test that MusicHistory's constructor is raising exception when called with wrong parameters.

    Parameters
    ----------
    song_entries : list[mh.SongEntry]
        List of SongEntry instances that will be used to initialize the object.
    '''
    with pytest.raises(mh.MusicHistoryTypeError):
        mh.MusicHistory(song_entries)


@pytest.mark.parametrize('songs_param', [[('metal', 10)]])
def test_music_history_len(songs, times_played, songs_param: list[tuple[str, int]]):
    '''
    Test MusicHistory's len method.

    Parameters
    ----------
    songs : fixture
        Fixture that returns a list of songs.
    times_played : fixture
        Fixture that returns a list of dates.
    songs_param : list[tuple[str,int]]
        List composed of tuples of str and int, being the string the name of the music
        genre and the int the number of songs (up to 10) that will be added from that
        music genre to the MusicHistory object returned.
    '''
    song_entries = [mh.SongEntry(song, times_played) for song in songs(songs_param)]
    music_history = mh.MusicHistory(song_entries)
    assert_that(music_history).is_length(songs_param[0][1])


@pytest.mark.parametrize('songs_param', [
    [('metal', 10)],
    [('metal', 10), ('rock', 4)],
])
def test_music_history_genres_listened(songs, times_played, songs_param: list[tuple[str, int]]):
    '''
    Test MusicHistory's genres_listened property.

    Parameters
    ----------
    songs : fixture
        Fixture that returns a list of songs.
    times_played : fixture
        Fixture that returns a list of dates.
    songs_param : list[tuple[str,int]]
        List composed of tuples of str and int, being the string the name of the music
        genre and the int the number of songs (up to 10) that will be added from that
        music genre to the MusicHistory object returned.
    '''
    song_entries = [mh.SongEntry(song, times_played) for song in songs(songs_param)]
    music_history = mh.MusicHistory(song_entries)
    assert_that(music_history.genres_listened).is_equal_to({x.genre for x in song_entries})


@pytest.mark.parametrize('songs_param', [
    [('metal', 10)],
    [('metal', 10), ('rock', 4)],
])
def test_music_history_total_entries(songs, times_played, songs_param: list[tuple[str, int]]):
    '''
    Test MusicHistory's total_entries property.

    Parameters
    ----------
    songs : fixture
        Fixture that returns a list of songs.
    times_played : fixture
        Fixture that returns a list of dates.
    songs_param : list[tuple[str,int]]
        List composed of tuples of str and int, being the string the name of the music
        genre and the int the number of songs (up to 10) that will be added from that
        music genre to the MusicHistory object returned.
    '''
    song_entries = [mh.SongEntry(song, times_played) for song in songs(songs_param)]
    music_history = mh.MusicHistory(song_entries)
    assert_that(music_history.total_entries).is_equal_to(len(song_entries)*len(times_played))


@pytest.mark.parametrize('songs_param, times_played, preferences', [
    ([('metal', 10)], [valid_date()], {
        'metalcore': 0.1,
        'heavy': 0.2,
        'metal': 0.2,
        'trash': 0.1,
        'doom': 0.1,
        'djent': 0.1,
        'blackgaze': 0.1,
        'nu-metal': 0.1
    }),
    ([('metal', 10), ('rock', 4)], [valid_date()], {
        'metalcore': 0.071,
        'heavy': 0.142,
        'metal': 0.142,
        'trash': 0.071,
        'doom': 0.071,
        'djent': 0.071,
        'blackgaze': 0.071,
        'nu-metal': 0.071,
        'rock': 28.57
    }),
])
def test_music_history_genre_preferences(songs, songs_param: list[tuple[str, int]],
                                         times_played: list[datetime],
                                         preferences: dict[str:float],
                                         float_tolerance: float):
    '''
    Test MusicHistory's genre_preferences method.

    Parameters
    ----------
    songs : fixture
        Fixture that returns a list of songs.
    songs_param : list[tuple[str,int]]
        List composed of tuples of str and int, being the string the name of the music
        genre and the int the number of songs (up to 10) that will be added from that
        music genre to the MusicHistory object returned.
    times_played : list[datetime]
        List with the dates when each song was played.
    preferences : dict[str:float]
        The expected computed preferences.
    float_tolerance : float
        Number that sets the appropriate deviation when comparing floating numbers.
    '''
    song_entries = [mh.SongEntry(song, times_played) for song in songs(songs_param)]
    music_history = mh.MusicHistory(song_entries)
    genres = music_history.genres_listened
    mh_preferences = music_history.genre_preferences
    map(lambda x: assert_that(mh_preferences[x]).is_close_to(
        preferences[x], float_tolerance), genres)
