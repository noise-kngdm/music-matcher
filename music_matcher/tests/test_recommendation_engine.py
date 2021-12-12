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
def test_recommendation_init(songs, users, user_names):
    
    users = [users(username, songs) for username in user_names]
    engine = rec.RecommendationEngine(GENRES_PATH, users)
    assert_that(engine).is_type_of(rec.RecommendationEngine)


@pytest.mark.parametrize('genres_path,user_names,expected_exception', [
    (GENRES_PATH, ['lucia'], rec.RecommendationError),
    (None, ['lucia', 'luis', 'daniel'], rec.RecommendationTypeError),
    ('unexisting_file', ['lucia', 'luis', 'daniel'], rec.RecommendationFileError),
    (WRONG_GENRES_PATH, ['lucia', 'luis', 'daniel'], rec.RecommendationParsingError)
])
def test_recommendation_init_ko(songs, users, genres_path, user_names,
                                expected_exception):
    users = [users(username, songs) for username in user_names]
    with pytest.raises(expected_exception):
        rec.RecommendationEngine(genres_path, users)


@pytest.fixture
def loaded_genres():
    genres, _ = rec.RecommendationEngine.load_yaml_file(GENRES_PATH)
    return genres


@pytest.mark.parametrize('preferences,normalized_preferences', [
    [{'metal': 0.3}, {'metal': 0.3}],
    [{'heavy': 0.2, 'black': 0.3},
     {'metal': 0.5}],
    [{'hardcore': 0.7, 'opera': 0.1, 'medieval': 0.1, 'rap': 0.1},
     {'punk': 0.7, 'classical': 0.2, 'hip-hop': 0.1}],
])
def test_recommendation_normalize(monkeypatch, preferences, float_tolerance,
                                  normalized_preferences, loaded_genres):
    def fake_init(obj, **kwargs):
        pass
    monkeypatch.setattr(rec.RecommendationEngine, '__init__', fake_init)

    rec_eng = rec.RecommendationEngine(genres_yaml=None, users=None)
    rec_eng._genres = loaded_genres
    computed_preferences = rec_eng._normalize_preferences(preferences)
    used_keys = 0

    for k, v in computed_preferences.items():
        if k in normalized_preferences:
            assert_that(v).is_close_to(normalized_preferences[k], float_tolerance)
            used_keys += 1
        else:
            assert_that(v).is_close_to(0.0, float_tolerance)

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
def test_recommendation_calculate_affinity(pref_1, pref_2, expected_affinity,
                                           float_tolerance):
    computed_affinity = rec.RecommendationEngine._calculate_affinity(pref_1,pref_2)
    assert_that(computed_affinity).is_close_to(expected_affinity, float_tolerance)



@pytest.mark.parametrize('user_names,users_compared, expected_result', [
    (['lucia', 'luis'], ['lucia', 'luis'], 0.1518),
    (['daniel', 'lucia', 'luis'], ['daniel', 'luis'], 0.2645),
    (['daniel', 'lucia', 'luis', 'jorge'], ['lucia', 'luis'], 0.1518),
])
def test_recommendation_affinity(songs, users, user_names, users_compared,
                                 expected_result, float_tolerance):
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
    users = [users(username, songs) for username in user_names]
    rec_en = rec.RecommendationEngine(GENRES_PATH, users)
    for i in range(len(rec_en._matrix)):
        for j in range(len(rec_en._matrix)):
            assert_that(rec_en._matrix[i][j]).is_close_to(expected_matrix[i][j], float_tolerance)
