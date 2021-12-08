import pytest
from assertpy import assert_that

import music_matcher.recommendation_engine as rec


genres_path = 'music_matcher/data/music_genres.yaml'
wrong_genres_path = 'music_matcher/tests/data/wrong_genres.yaml'


@pytest.mark.parametrize('user_names', [
    ['lucia', 'luis'],
    ['lucia', 'luis', 'jorge', 'daniel']
])
def test_recommendation_init(songs, users, user_names):
    users = [users(username, songs) for username in user_names]
    engine = rec.RecommendationEngine(genres_path, users)
    assert_that(engine).is_type_of(rec.RecommendationEngine)


@pytest.mark.parametrize('genres_path,user_names,expected_exception', [
    (genres_path, ['lucia'], rec.RecommendationError),
    (None, ['lucia', 'luis', 'daniel'], rec.RecommendationTypeError),
    ('unexisting_file', ['lucia', 'luis', 'daniel'], rec.RecommendationError),
    (wrong_genres_path, ['lucia', 'luis', 'daniel'], rec.RecommendationParsingError)
])
def test_recommendation_init_ko(songs, users, genres_path, user_names,
                                expected_exception):
    users = [users(username, songs) for username in user_names]
    with pytest.raises(expected_exception):
        rec.RecommendationEngine(genres_path, users)


def test_recommendation_normalize():
    pass
