# Holds saved program data which we want to be persistent when we close and open the program.
# This is ONLY read from ONCE when launching and written to ONCE when closing. (Probably.)
class SaveData:

    # Eventually, we hope to support multiple keys for different APIs, and the ability to enter your own key.
    key = 'a1078617'

    # We only bother storing titles to populate the main listbox so it looks good, without having to
    # spam the API for every film in the wishlist every time we open the program.
    # But we actually use the IDs to query the database when we select something in the listbox.
    # Obviously one magical day we'll be able to enter our own.
    films = [
        ['tt0133093', 'The Matrix'],
        ['tt0317705', 'The Incredibles'],
        ['tt1270797', 'Venom']
    ]
