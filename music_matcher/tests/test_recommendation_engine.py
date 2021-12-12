'''Tests for the recommendation_engine.py file.'''

import pytest
from assertpy import assert_that

import music_matcher.recommendation_engine as rec


GENRES_PATH = 'music_matcher/data/music_genres.yaml'
WRONG_GENRES_PATH = 'music_matcher/tests/data/wrong_genres.yaml'

@pytest.mark.parametrize('user_names', [
    ['lucia', 'luis'],
    ['lucia', 'luis', 'jorge', 'daniel']
])
def test_recommendation_init(songs, users, user_names: list[str]):
    """
    Test that User's constructor is working.

    Parameters
    ----------
    songs : fixture
        Song's factory as fixture.
    users : fixture
        User's factory as fixture.
    user_names : list[str]
        List of the usernames that should be tested in each execution.
    """
    users = [users(username, songs) for username in user_names]
    engine = rec.RecommendationEngine(GENRES_PATH, users)
    assert_that(engine).is_type_of(rec.RecommendationEngine)


@pytest.mark.parametrize('genres_path,user_names,expected_exception', [
    (GENRES_PATH, ['lucia'], rec.RecommendationError),
    (None, ['lucia', 'luis', 'daniel'], rec.RecommendationTypeError),
    ('unexisting_file', ['lucia', 'luis', 'daniel'], rec.RecommendationFileError),
    (WRONG_GENRES_PATH, ['lucia', 'luis', 'daniel'], rec.RecommendationParsingError)
])
def test_recommendation_init_ko(songs, users, genres_path: str, user_names: list[str],
                                expected_exception: Exception):
    """
    Test that User's constructor is raising exception when called with wrong parameters.

    Parameters
    ----------
    songs : fixture
        Song's factory as fixture.
    users : fixture
        User's factory as fixture.
    genres_path : str
        The path where the yaml file with the genres is located in.
    user_names : list[str]
        List of the usernames that should be tested in each execution.
    expected_exception : Exception
        The exception that should be raised.
    """
    users = [users(username, songs) for username in user_names]
    with pytest.raises(expected_exception):
        rec.RecommendationEngine(genres_path, users)


@pytest.fixture
def loaded_genres():
    """Return the genres and subgenres in a yaml file.

    Returns
    -------
    set[rec.Genre]
        A set with the genres included in the yaml file.
    """
    genres, _ = rec.RecommendationEngine.load_yaml_file(GENRES_PATH)
    return genres


@pytest.mark.parametrize('preferences,normalized_preferences', [
    [{'metal': 0.3}, {'metal': 0.3}],
    [{'heavy': 0.2, 'black': 0.3},
     {'metal': 0.5}],
    [{'hardcore': 0.7, 'opera': 0.1, 'medieval': 0.1, 'rap': 0.1},
     {'punk': 0.7, 'classical': 0.2, 'hip-hop': 0.1}],
])
def test_recommendation_normalize(monkeypatch, preferences: dict[str:float], float_tolerance,
                                  normalized_preferences: dict[str:float], loaded_genres):
    """
    Test the RecommendationEngine's _normalize_preferences method.

    Parameters
    ----------
    monkeypatch : fixture
        Fixture that will be used to monkeypatch some aspects of the execution.
    preferences : dict[str:float]
        Dictionary of genres and percentage before normalization.
    float_tolerance : float
        Number that sets the appropriate deviation when comparing floating numbers.
    normalized_preferences : dict[str:float]
        Dictionary with the expected result of normalizing the preferences parameter.
    loaded_genres : fixture
        Fixture that returns the set of rec.Genres used.
    """
    def fake_init(*args, **kwargs):
        pass
    monkeypatch.setattr(rec.RecommendationEngine, '__init__', fake_init)

    rec_eng = rec.RecommendationEngine(genres_yaml=None, users=None)
    rec_eng._genres = loaded_genres
    computed_preferences = rec_eng._normalize_preferences(preferences)
    used_keys = 0

    for k, val in computed_preferences.items():
        if k in normalized_preferences:
            assert_that(val).is_close_to(normalized_preferences[k], float_tolerance)
            used_keys += 1
        else:
            assert_that(val).is_close_to(0.0, float_tolerance)

    assert_that(used_keys).is_equal_to(len(normalized_preferences))


@pytest.mark.parametrize('pref_1,pref_2,expected_affinity', [
    ({'metal': 0.1, 'rock': 0.2, 'jazz': 0.0},
     {'jazz': 0.2, 'rock': 0.1, 'metal': 0.0},
     0.02),
    ({'metal': 0.1, 'rock': 0.2, 'jazz': 0.1},
     {'jazz': 0.7, 'rock': 0.1, 'metal': 0.0},
     0.09),
    ({'metal': 0.1, 'rock': 0.2, 'jazz': 0.1, 'classical': 0.6},
     {'jazz': 0.7, 'rock': 0.1, 'metal': 0.0, 'classical': 0.2},
     0.21),
])
def test_recommendation_calculate_affinity(pref_1: dict[str:float], pref_2: dict[str:float],
                                           expected_affinity: float, float_tolerance):
    """
    Test the RecommendationEngine's _calculate_affinity method.

    Parameters
    ----------
    pref_1 : dict[str:float]
        Preferences of the user 1.
    pref_2 : dict[str:float]
        Preferences of the user 2.
    expected_affinity : float
        Affinity that both users should have after the calculation.
    float_tolerance : float
        Number that sets the appropriate deviation when comparing floating numbers.
    """
    computed_affinity = rec.RecommendationEngine._calculate_affinity(pref_1,pref_2)
    assert_that(computed_affinity).is_close_to(expected_affinity, float_tolerance)



@pytest.mark.parametrize('user_names,users_compared, expected_result', [
    (['lucia', 'luis'], ['lucia', 'luis'], 0.1518),
    (['daniel', 'lucia', 'luis'], ['daniel', 'luis'], 0.2645),
    (['daniel', 'lucia', 'luis', 'jorge'], ['lucia', 'luis'], 0.1518),
])
def test_recommendation_affinity(songs, users, user_names: list[str],
                                 users_compared: list[str], expected_result: float,
                                 float_tolerance):
    """
    Test the RecommendationEngine's affinity computing results.

    Parameters
    ----------
    songs : fixture
        Song's factory as fixture.
    users : fixture
        User's factory as fixture.
    user_names : list[str]
        Usernames that will be used to initialize the RecommendationEngine instance.
        They must be included in the users() fixture.
    users_compared : list[str]
        List with the two users whose affinity is going to be requested.
    expected_result : float
        The expected affinity between the two users chosen to compare then.
    float_tolerance : float
        Number that sets the appropriate deviation when comparing floating numbers.
    """
    users = [users(username, songs) for username in user_names]
    rec_en = rec.RecommendationEngine(GENRES_PATH, users)
    requested_users = [x for x in users if x.username in users_compared]
    computed_affinity = rec_en.affinity(tuple(requested_users))
    assert_that(computed_affinity).is_close_to(expected_result, float_tolerance)


@pytest.mark.parametrize('user_names, expected_matrix', [
    (['lucia', 'luis'], [[1, 0.1518], [0.1518, 1]]),
])
def test_recommendation_init_affinity_matrix(songs, users, user_names,
                                             expected_matrix, float_tolerance):
    """
    Test the RecommendationEngine's _initialize_affinity_matrix method.

    Parameters
    ----------
    songs : fixture
        Song's factory as fixture.
    users : fixture
        User's factory as fixture.
    user_names : list[str]
        Usernames that will be used to initialize the RecommendationEngine instance.
    expected_matrix : list[float]
        The matrix that should be set as the _matrix attribute in the RecommendationEngine instance.
    float_tolerance : float
        Number that sets the appropriate deviation when comparing floating numbers.
    """
    users = [users(username, songs) for username in user_names]
    rec_en = rec.RecommendationEngine(GENRES_PATH, users)
    for i, row in enumerate(rec_en._matrix):
        for j, elem in enumerate(row):
            assert_that(elem).is_close_to(expected_matrix[i][j], float_tolerance)
