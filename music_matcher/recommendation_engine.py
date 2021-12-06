from sys import exit
from yaml import load, YAMLError

import User


class RecommendationError(ValueError):
    pass


class RecommendationEngine:
    """Calculate the affinity of users based on  their most listened genres."""
    def __init__(self, genres_yaml: str, users: set[User]):
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
        try:
            with open(genres_yaml, 'r') as f:
                yaml_file = load(f)['genres']
                self._genres = yaml_file['genres']
                self._yaml_version = yaml_file['version']
        except OSError as e:
            print(f"ERROR while opening the {genres_yaml} file: {e}")
        except YAMLError as e:
            print(f"Error while loading the {genres_yaml} file: {e}")
            exit(1)

        self._preferences = [(user, self._normalize_preferences(user.music_history.genre_preferences))
                             for user in users]

        self._affinity_matrix = RecommendationEngine._initialize_affinity_matrix()

    def _normalize_preferences(self, preferences: dict[str:float]) -> dict[str: float]:
        normalized = {key: 0.0 for key in self._genres.keys()}
        for user_genre, percentage in preferences.items():
            for genre, data in self._genres.items():
                if user_genre == genre or user_genre in data['subgenres']:
                    normalized[genre] += percentage

    @classmethod
    def _calculate_affinity(user1: dict[str:float],
                            user2: dict[str:float]) -> float:
        percentages_1 = user1.values()
        percentages_2 = user2.values()
        affinity_list = [percentages_1[i]*percentages_2[i]
                         for i in range(len(user1))]

        return sum(affinity_list)

    def _initialize_affinity_matrix(self) -> list[list[float]]:
        num_users = len(self._preferences)
        self._matrix = [[0] * len(num_users)] * len(self.num_users)
        for i in range(len(num_users)):
            self._matrix[i][i] = 1

        for i in range(len(num_users)):
            preference_1 = self._preferences[i]
            for j in range(i+1, len(num_users)):
                preference_2 = self._preferences[j]
                affinity = RecommendationEngine.calculate_affinity(preference_1[1],
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
