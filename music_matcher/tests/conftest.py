from datetime import datetime, timedelta
from functools import lru_cache

import pytest

import music_matcher.song as song
import music_matcher.music_history as mh
from music_matcher.user import User


@lru_cache
def genres():
    return ['metal', 'rock', 'punk', 'pop', 'classical', 'hip-hop',
            'electronic']


@pytest.fixture
def songs():
    def _return_songs(genres: list[tuple[str, int]]):
        songs = {
            'metal': [
                song.Song('Turning Point', 'metalcore', 'Killswitch Engage', 2013),
                song.Song('Holy Diver', 'heavy', 'Dio', 1983),
                song.Song('Paranoid', 'metal', 'Black Sabbath', 1970),
                song.Song('War Pigs', 'metal', 'Black Sabbath', 1970),
                song.Song('Tornado Of Souls', 'trash', 'Megadeth', 1990),
                song.Song('A Solitary Reign', 'doom', 'Amenra', 2017),
                song.Song('Bleed', 'djent', 'Meshuggah', 2008),
                song.Song('Freak On a Leash', 'nu-metal', 'Korn', 1998),
                song.Song('Hallowed Be Thy Name', 'heavy', 'Iron Maiden', 1982),
                song.Song('Dream House', 'blackgaze', 'Deafheaven', 2013)
            ],
            'rock': [
                song.Song('All Along the Watchtower', 'rock', 'Jimi Hendrix', 1968),
                song.Song('Stairway to Heaven', 'rock', 'Led Zeppelin', 1971),
                song.Song('Bouquet (Fuego y Mierda)', 'rock', 'Cuchillo de Fuego', 2015),
                song.Song('You Drive Me Wild', 'rock', 'The Runaways', 1976),
                song.Song('Paranoid Android', 'alternative rock', 'Radiohead', 1997),
                song.Song('High Hopes', 'progressive', 'Pink Floyd', 1994),
                song.Song('Roundabout', 'progressive', 'Yes', 1971),
                song.Song('Epitaph', 'progressive', 'King Crimson', 1969),
                song.Song('Riders on the Storm', 'rock', 'The Doors', 1971),
                song.Song('T.N.T.', 'hard', 'AC/DC', 1976),
            ],
            'punk': [
                song.Song('Tannhäuser', 'screamo', 'Catorce', 2019),
                song.Song('Annapurnas', 'screamo', 'Viva Belgrado', 2016),
                song.Song('Blitzkrieg Bop', 'punk', 'The Ramones', 1976),
                song.Song('Anarchy in the UK', 'punk', 'Sex Pistols', 1976),
                song.Song('I Fall', 'punk', 'The Damned', 1977),
                song.Song('(I’m) Stranded', 'punk', 'The Saints', 1977),
                song.Song('White Riot', 'punk', 'The Clash', 1977),
                song.Song('Sheena is a Punk Rocker', 'punk', 'The Ramones', 1977),
                song.Song('God Save the Queen', 'punk', 'Sex Pistols', 1977),
                song.Song('Pretty Vacant', 'punk', 'Sex Pistols', 1977),
                song.Song('Hong Kong Garden', 'gothic', 'Siouxsie and the Banshees', 1978),
            ],
            'jazz': [
                song.Song('Take the A Train', 'jazz', 'Duke Ellington', 1940),
                song.Song('So What', 'jazz', 'Miles Davis', 1959),
                song.Song('Giant Steps', 'jazz', 'John Coltrane', 1960),
                song.Song('One O’Clock Jump', 'jazz', 'Count Basie and his Orchestra', 1937),
                song.Song('Strange Fruit', 'jazz', 'Billie Holiday', 1939),
                song.Song('What A Wonderful World', 'jazz', 'Louis Armstrong', 1967),
                song.Song('Dave Brubeck Quartet', 'jazz', 'Take Five', 1959),
                song.Song('The Sidewinder', 'jazz', 'Lee Morgan', 1965),
                song.Song('Goodbye Pork Pie Hat', 'jazz', 'Charles Mingus', 1959),
                song.Song('My Funny Valentine', 'jazz', 'Chet Baker', 1954),
            ],
            'pop': [
                song.Song('Hey Jude', 'pop', 'The Beatles', 1968),
                song.Song('Marta, Sebas, Guille y los demás', 'pop', 'Amaral', 2005),
                song.Song('Your Song', 'pop', 'Elton John', 1970),
                song.Song('Please, please, please, let me get what I want', 'indie pop', 'The Smiths', 1984),
                song.Song('We are the world', 'pop', 'Michael Jackson', 1985),
                song.Song('Hallelujah', 'pop', 'Jeff Buckley', 1994),
                song.Song('Stand by me', 'pop', 'Oasis', 1997),
                song.Song('Rosas', 'pop', 'La Oreja de Van Gogh', 2003),
                song.Song('Single Ladies (Put a Ring on It)', 'pop', 'Beyoncé', 2008),
                song.Song('Umbrella', 'pop', 'Rihanna', 2008),
                song.Song('Toxic', 'pop', 'Britney Spears', 2003),
            ],
            'classical': [
                song.Song('Eine kleine Nachtmusik', 'classical', 'Mozart', 1787),
                song.Song('Für Elise', 'classical', 'Beethoven', 1810),
                song.Song('O mio babbino caro', 'classical', 'Puccini', 1918),
                song.Song('Moonlight', 'classical', 'Beethoven', 1801),
                song.Song('Symphony No. 5 in C minor, Op. 67', 'classical', 'Beethoven', 1808),
                song.Song('Messiah', 'classical', 'Handel', 1741),
                song.Song('Eine kleine Nachtmusik', 'classical', 'Mozart', 1787),
                song.Song('The Blue Danube', 'classical', 'Johan Strauss', 1866),
                song.Song('Introduction, or Sunrise', 'classical', 'Richard Strauss', 1896),
                song.Song('Nutcracker', 'classical', 'Tchaikovsky', 1892),
                song.Song('Rite of Spring', 'classical', 'Stravinsky', 1913),
            ],
            'hip-hop': [
                song.Song('Juicy', 'hip-hop', 'Notorious B.I.G.', 1994),
                song.Song('Fight The Power', 'hip-hop', 'Public Enemy', 1989),
                song.Song('Shook Ones (Part II)', 'hip-hop', 'Mobb Deep', 1995),
                song.Song('The Message', 'hip-hop', 'Grandmaster Flash & The Furious Five', 1982),
                song.Song('C.R.E.A.M.', 'hip-hop', 'Wu Tang Clan', 1993),
                song.Song('Nuthin’ But A ‘G’ Thang', 'hip-hop', 'Snoop Dogg', 1992),
                song.Song('Jugador 9', 'trap', 'Soto Asa', 2021),
                song.Song('Solo', 'trap', 'Sticky M.A.', 2019),
                song.Song('I can\'t get it out', 'rap', 'Agorazein', 2011),
                song.Song('METALLICA', 'trap', 'Yung Beef', 2021),
                song.Song('Lisístrata', 'rap', 'Gata Cattana', 2012),
            ],
            'electronic': [
                song.Song('Strobe', 'electronic', 'deadmau5', 2009),
                song.Song('Digital Love', 'electronic', 'Daft Punk', 2001),
                song.Song('Levels', 'electronic', 'Avicii', 2011),
                song.Song('Animals', 'electronic', 'Martin Garrix', 2013),
                song.Song('Feel So Close', 'electronic', 'Calvin Harris', 2012),
                song.Song('Get Lucky', 'electronic', 'Daft Punk', 2013),
                song.Song('One more Time', 'electronic', 'Daft Punk', 2000),
                song.Song('Fire Stone', 'electronic', 'Kygo', 2014),
                song.Song('SuperLove ft. Lenny Kravitz', 'electronic', 'Avicii', 2011),
                song.Song('Greyhound', 'electronic', 'Swedish House Mafia', 2012),
                song.Song('WTF Is In My Cup', 'electronic', 'Chico Blanco', 2018),
            ]
        }
        return [entry for genre, number in genres for entry in songs[genre][:number]]
    return _return_songs


@pytest.fixture(params=[[('metal', 10), ('rock', 4), ('hip-hop', 1)]])
def lucia_music_history(songs, request):
    init_songs = songs(request.param)
    song_entries = [mh.SongEntry(init_songs[i],
                                            [datetime.fromisoformat('2020-01-01')
                                             + timedelta(days=i)])
                    for i in range(len(init_songs))]
    return mh.MusicHistory(song_entries)


@pytest.fixture
def float_tolerance() -> float:
    '''Return the tolerance used to compare floating numbers.

    Returns
    -------
    float
        Tolerance that will be used.
    '''
    return 0.001


@pytest.fixture
def users():
    def _return_users(name: str, songs: callable):
        '''
        Return an initialized user.

        Parameters
        ----------
        name : str
            The name of the user required. Must be one of the keys of
            the 'users' dictionary.
        songs : callable
            The function returned by the songs factory as fixture.
        '''
        users = {
            'lucia': {
                'username': 'lucia',
                'name': 'Lucía Manson',
                'gender': 'W',
                'birthdate': '2000-03-23',
                'music_history':
                    [('metal', 10),
                     ('rock', 4),
                     ('hip-hop', 1)],

            },
            'luis': {
                'username': 'luis',
                'name': 'Luis',
                'gender': 'O',
                'birthdate': '2000-07-03',
                'music_history':
                    [('rock', 10),
                     ('hip-hop', 1),
                     ('pop', 7)]
            },
            'jorge': {
                'username': 'jorge',
                'name': 'Jorge',
                'gender': 'M',
                'birthdate': '1970-12-15',
                'music_history':
                    [('punk', 10),
                     ('rock', 4)]
            },
            'daniel': {
                'username': 'daniel',
                'name': 'Daniel',
                'gender': 'NB',
                'birthdate': '1996-08-05',
                'music_history':
                    [('metal', 8),
                     ('rock', 10),
                     ('jazz', 3)]
            },
        }
        song_date = valid_date()
        user = users[name]
        song_entries = [mh.SongEntry(song, [song_date])
                        for song in songs(user['music_history'])]
        del user['music_history']

        return User(**user, music_history=mh.MusicHistory(song_entries))

    return _return_users


def valid_date() -> datetime:
    return datetime.fromisoformat('2001-12-01')
