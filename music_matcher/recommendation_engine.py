from dataclasses import dataclass

from yaml import safe_load, YAMLError

from music_matcher.user import User


class RecommendationError(ValueError):
    pass


class RecommendationTypeError(TypeError):
    pass


class RecommendationParsingError(YAMLError):
    pass


@dataclass(frozen=True)
class Genre:
    '''
    Class that encapsulates a genre and its subgenres according to
    the data model's representation.
    '''
    basic_genre: str
    subgenres: frozenset[str]


class RecommendationEngine:
    """Calculate the affinity of users based on  their most listened genres."""

    MIN_NUM_USERS = 2

    def __init__(self, genres_yaml: str, users: list[User]):
        """
        RecommendationEngine constructor.

        Parameters
        ----------
        genres_yaml : str
            File containing information about the valid genres and their
            respective subgenres.
        users : set(User)
            Set contaning the users whose affinity should be calculated.
        """
        if not isinstance(users, list):
            raise RecommendationTypeError(
                'The users parameter must be of type list,'
                f' and not {type(users)}')

        if not isinstance(genres_yaml, str):
            raise RecommendationTypeError(
                'The genres_yaml parameter must be of type str,'
                f' and not {type(genres_yaml)}')

        for x in users:
            if not isinstance(x, User):
                raise RecommendationTypeError(
                    'Every item in users must be of type User,'
                    f' and not {type(x)}')

        if not len(users) >= RecommendationEngine.MIN_NUM_USERS:
            raise RecommendationError(
                'The minimum number of users needed is '
                f'{RecommendationEngine.MIN_NUM_USERS}')

        try:
            with open(genres_yaml, 'r') as f:
                yaml_file = safe_load(f)
                try:
                    self._genres = {Genre(genre, frozenset(subgenres[0]['subgenres']))
                                    for x in yaml_file['genres']
                                    for genre, subgenres in x.items()}
                except TypeError as e:
                    raise RecommendationParsingError(
                        'Error while parsing the yaml file, check that it has '
                        f'a valid syntax: {e}')

                self._yaml_version = yaml_file['version']
        except OSError as e:
            raise RecommendationError(f'Error while opening the {genres_yaml} file: {e}')
        except YAMLError as e:
            raise(RecommendationParsingError(
                f"Error while loading the {genres_yaml} file: {e}"))

        self._preferences = [(user, self._normalize_preferences(user.music_history.genre_preferences))
                             for user in users]

        self._initialize_affinity_matrix()

    def _normalize_preferences(self, preferences: dict[str:float]) -> dict[str: float]:
        normalized = {genre.basic_genre: 0.0 for genre in self._genres}
        for user_genre, percentage in preferences.items():
            for genre in self._genres:
                if user_genre == genre or user_genre in genre.subgenres:
                    normalized[genre.basic_genre] += percentage
                    break
        return normalized

    @classmethod
    def _calculate_affinity(cls, user1: dict[str:float],
                            user2: dict[str:float]) -> float:
        percentages_1 = list(user1.values())
        percentages_2 = list(user2.values())
        affinity_list = [percentages_1[i]*percentages_2[i]
                         for i in range(len(user1))]

        return sum(affinity_list)

    def _initialize_affinity_matrix(self) -> list[list[float]]:
        num_users = len(self._preferences)
        self._matrix = [[0] * num_users] * num_users
        for i in range(num_users):
            self._matrix[i][i] = 1

        for i in range(num_users):
            preference_1 = self._preferences[i]
            for j in range(i+1, num_users):
                preference_2 = self._preferences[j]
                affinity = RecommendationEngine._calculate_affinity(preference_1[1],
                                                                    preference_2[1])
                self._matrix[i][j] = affinity
                self._matrix[j][i] = affinity

    def affinity(self, user1: User, user2: User) -> float:
        """
        Return the affinity between two users.

        Parameters
        ----------
        user1 : User
            First user.
        user2 : User
            Second user.

        Returns
        -------
        float
            The affinity calculated by the RecommendationEngine

        Raises
        ------
        RecommendationError
            When any of the users specified is not amongst the available data.
        """
        try:
            i = [x for x in self._preferences if x[0] == user1][0]
            j = [x for x in self._preferences if x[0] == user2][0]
            return self._matrix[i][j]

        except IndexError as e:
            raise RecommendationError(f'The users specified doesn\'t exist in the database: {e}')
