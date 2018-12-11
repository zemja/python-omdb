from pathlib import Path

import pickle
import os.path

# Holds saved program data which we want to be persistent when we close and open the program.
# This is ONLY read from ONCE when launching and written to ONCE when closing. (Probably.)
class SaveData:

    # NOTE This tries to open the data file. If it's not found, we just use default values. If
    # there's any other exception, the caller should catch it.
    def __init__(self):

        # False if we couldn't load the file for some reason and are just using defaults. True if we
        # loaded OK.
        self.from_file = False

        self.path = os.path.join(Path.home(), '.python-omdb')

        self.keys = {
            'omdb': None,
            'tmdb': None
        }

        # Should be [['ID', 'Title'], ['ID', 'Title'] ...etc... ]
        self.films = []

        try:
            with open(self.path, 'rb') as file:
                # Some things will be set and some things won't if this fails towards the end, but oh well.
                data = pickle.load(file)
                self.keys  = data.keys
                self.films = data.films
                # self = pickle.load(file)
        except FileNotFoundError:
            return

        self.from_file = True

    # NOTE: Caller handles file exceptions.
    def save(self):
        with open(self.path, 'wb') as file:
            pickle.dump(self, file)
