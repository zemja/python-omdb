from pathlib import Path

import pickle
import os.path

# Holds saved program data which we want to be persistent when we close and open the program.
# This is ONLY read from ONCE when launching and written to ONCE when closing. (Probably.)
class SaveData:

    # NOTE This tries to open the data file. If it's not found, we just use default values. If
    # there's any other exception, the caller should catch it.
    def __init__(self):

        self.path = os.path.join(Path.home(), '.python-omdb')

        # TODO Eventually, these will default to None and []. If you try to get films without a key, it
        # will nag you to enter them.

        # Eventually, we hope to support multiple keys for different APIs, and the ability to enter your own key.
        self.key = 'a1078617'

        # We only bother storing titles to populate the main listbox so it looks good, without having to
        # spam the API for every film in the wishlist every time we open the program.
        # But we actually use the IDs to query the database when we select something in the listbox.
        # Obviously one magical day we'll be able to enter our own.
        self.films = [
            ['tt0133093', 'The Matrix'],
            ['tt0317705', 'The Incredibles'],
            ['tt1270797', 'Venom']
        ]

        try:
            with open(self.path, 'rb') as file:
                data = pickle.load(file)
                self.key = data.key
                self.films = data.films
                # self = pickle.load(file)
        except FileNotFoundError:
            pass

    # NOTE: Caller handles file exceptions.
    def save(self):
        with open(self.path, 'wb') as file:
            pickle.dump(self, file)
