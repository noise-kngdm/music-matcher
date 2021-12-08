from datetime import datetime, timedelta

import pytest
from assertpy import assert_that

import music_matcher.music_history as mh
from .conftest import genres, valid_date
from music_matcher.song import Song


length_genres = len(genres())


@pytest.fixture(params=[(genres(), i) for i in range(length_genres)])
def get_song(songs, request):
    genres = request.param[0]
    index = request.param[1]
    return songs([(genres[index], 1), ])[0]


def test_song_entry_init(get_song):
    song_entry = mh.SongEntry(get_song, [valid_date()])
    assert_that(song_entry).is_type_of(mh.SongEntry)


def valid_song() -> Song:
    return Song('Lake Fantasy', 'blackgaze', 'Lantlôs', 2021)


@pytest.mark.parametrize('song, times_played', [
    (None, None),
    (valid_song(), [False]),
    (valid_song(), [valid_date(), 1]),
    (None, [valid_date()])
])
def test_song_entry_init_ko(song, times_played):
    with pytest.raises(mh.SongEntryTypeError):
        mh.SongEntry(song, times_played)


def test_song_entry_genre(get_song):
    song_entry = mh.SongEntry(get_song, [valid_date()])
    assert_that(song_entry.genre).is_equal_to(get_song.genre)


@pytest.fixture(params=[0, 3, 7])
def times_played(request):
    return [valid_date() - timedelta(days=i) for i in range(request.param)]


def test_song_entry_amount_reproductions(get_song, times_played):
    song_entry = mh.SongEntry(get_song, times_played)
    assert_that(song_entry.amount_reproductions).is_equal_to(len(times_played))


@pytest.mark.parametrize('songs_param', [[('metal', 10)]])
def test_music_history_init(songs, times_played, songs_param):
    song_entries = [mh.SongEntry(song, times_played) for song in songs(songs_param)]
    music_history = mh.MusicHistory(song_entries)
    assert_that(music_history).is_type_of(mh.MusicHistory)


@pytest.mark.parametrize('song_entries', [
    None,
    [False],
    [mh.SongEntry(valid_song(), [valid_date()]), False],
])
def test_music_history_init_ko(song_entries):
    with pytest.raises(mh.MusicHistoryTypeError):
        mh.MusicHistory(song_entries)


@pytest.mark.parametrize('songs_param', [[('metal', 10)]])
def test_music_history_len(songs, times_played, songs_param):
    song_entries = [mh.SongEntry(song, times_played) for song in songs(songs_param)]
    music_history = mh.MusicHistory(song_entries)
    assert_that(music_history).is_length(songs_param[0][1])


@pytest.mark.parametrize('songs_param', [
    [('metal', 10)],
    [('metal', 10), ('rock', 4)],
])
def test_music_history_genres_listened(songs, times_played, songs_param):
    song_entries = [mh.SongEntry(song, times_played) for song in songs(songs_param)]
    music_history = mh.MusicHistory(song_entries)
    assert_that(music_history.genres_listened).is_equal_to({x.genre for x in song_entries})


@pytest.mark.parametrize('songs_param', [
    [('metal', 10)],
    [('metal', 10), ('rock', 4)],
])
def test_music_history_total_entries(songs, times_played, songs_param):
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
def test_music_history_genre_preferences(songs, songs_param, times_played, preferences,
                                         float_tolerance):
    song_entries = [mh.SongEntry(song, times_played) for song in songs(songs_param)]
    music_history = mh.MusicHistory(song_entries)
    genres = music_history.genres_listened
    mh_preferences = music_history.genre_preferences
    map(lambda x: assert_that(mh_preferences[x]).is_close_to(preferences[x], float_tolerance), genres)
