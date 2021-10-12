class Profile:
    '''A class representing an user of the application.'''
    def __init__(self, age, name, gender, favourite_music_genre, favourite_artists, music_history):
        ''' 
        Profile class constructor.
            
            Attributes
            ----------
            age : int
                User's age.
            name : str
                User's name.
            gender : str
                User's gender.
            favourite_music_genre : str
                User's favourite music genre.
            favourite_artists : list of str
                User's favourite artists.
            music_history : MusicHistory object
                It will contains all the user music history.
        '''
        self.age = age
        self.name = name
        self.gender = gender
        self.favourite_music_genre = favourite_music_genre
        self.favourite_artists = favourite_artists
        self.music_history = music_history
