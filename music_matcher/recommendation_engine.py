"""Module that represents a RecommendationEngine."""

from dataclasses import dataclass

from yaml import safe_load, YAMLError

from music_matcher.user import User


class RecommendationError(ValueError):
    '''Exception that will be raised when the RecommendationEngine class
       has encountered a wrong value in the parameters of a method.'''


class RecommendationFileError(OSError):
    '''Exception that will be raised when a RecommendationEngine method
       is called using a wrong file path.'''


class RecommendationTypeError(TypeError):
    '''Exception that will be raised when a RecommendationEngine method
       is called using a parameter with a wrong type.'''


class RecommendationParsingError(YAMLError):
    '''Exception that will be raised when a RecommendationEngine method
       is called using a yaml file with a wrong format.'''


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
        users : list[User]
            Set contaning the users whose affinity should be calculated.

        Raises
        ------
        RecommendationTypeError
            When the type of any of the parameters is not the one expected.
        RecommendationError
            When the number of users is less than MIN_NUM_USERS.
        """
        if not isinstance(users, list):
            raise RecommendationTypeError(
                'The users parameter must be of type list,'
                f' and not {type(users)}')

        if not isinstance(genres_yaml, str):
            raise RecommendationTypeError(
                'The genres_yaml parameter must be of type str,'
                f' and not {type(genres_yaml)}')

        for user in users:
            if not isinstance(user, User):
                raise RecommendationTypeError(
                    'Every item in users must be of type User,'
                    f' and not {type(user)}')

        if not len(users) >= RecommendationEngine.MIN_NUM_USERS:
            raise RecommendationError(
                'The minimum number of users needed is '
                f'{RecommendationEngine.MIN_NUM_USERS}')

        self._genres, self._yaml_version = RecommendationEngine.load_yaml_file(genres_yaml)

        self._preferences = [(user.username,
                              self._normalize_preferences(user.music_history.genre_preferences))
                             for user in sorted(users)]

        self._initialize_affinity_matrix()

    @classmethod
    def load_yaml_file(cls, genres_yaml: str) -> set[Genre]:
        """
        Return a set of Genres and the version of a genres yaml file.

        Parameters
        ----------
        genres_yaml : str
            The path of the file from the root directory of the project.

        Returns
        -------
        genres : set[Genres]
            Set with the genres and subgenres loaded from the file.
        version : str
            Version of the genres_yaml file.

        Raises
        ------
        RecommendationParsingError
            When the format of the genres_yaml file is not valid.
        RecommendationFileError
            When the file could not be opened.
        """
        try:
            with open(genres_yaml, 'r', encoding='utf-8') as genres_file:
                yaml_file = safe_load(genres_file)
                try:
                    genres = {Genre(genre, frozenset(subgenres[0]['subgenres']))
                              for x in yaml_file['genres']
                              for genre, subgenres in x.items()}
                    version = yaml_file['version']
                except (TypeError, IndexError) as error:
                    raise RecommendationParsingError(
                        'Error while parsing the yaml file, check that it has '
                        f'a valid syntax: {error}') from error
        except OSError as error:
            raise RecommendationFileError(f'Error while opening the {genres_yaml}'
                                          ' file: {error}') from error
        except YAMLError as error:
            raise(RecommendationParsingError(
                f"Error while loading the {genres_yaml} file: {error}")) from error

        return genres, version

    def _normalize_preferences(self, preferences: dict[str:float]) -> dict[str:float]:
        normalized = {genre.basic_genre: 0.0 for genre in self._genres}
        for user_genre, percentage in preferences.items():
            for genre in self._genres:
                if user_genre == genre.basic_genre or user_genre in genre.subgenres:
                    normalized[genre.basic_genre] += percentage
                    break
        return normalized

    @classmethod
    def _calculate_affinity(cls, user1: dict[str:float], user2: dict[str:float]) -> float:
        percentages_1 = [user1[k] for k in sorted(user1.keys())]
        percentages_2 = [user2[k] for k in sorted(user2.keys())]
        affinity_list = [percentages_1[i]*percentages_2[i]
                         for i in range(len(user2))]

        return sum(affinity_list)

    def _initialize_affinity_matrix(self) -> list[list[float]]:
        num_users = len(self._preferences)
        self._matrix = [[0] * num_users for _ in range(num_users)]
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

    def _find_index(self, user: User) -> int:
        for i, elem in enumerate(self._preferences):
            if user.username == elem[0]:
                return i
        raise RecommendationError(f'The user specified {user.username} does not exists.')

    def affinity(self, users: tuple[User, User]) -> float:
        """
        Return the affinity between two users.

        Parameters
        ----------
        users : tuple[User, User]
            Users whose affinity is requested.

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
            i = self._find_index(users[0])
            j = self._find_index(users[1])
            return self._matrix[i][j]

        except IndexError as error:
            raise RecommendationError('The users specified doesn\'t exist'
                                      f'in the database: {error}') from error
