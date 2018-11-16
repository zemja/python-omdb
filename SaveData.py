# Holds saved program data which we want to be persistent when we close and open the program.
# This is ONLY read from ONCE when launching and written to ONCE when closing. (Probably.)
class SaveData:

    # Eventually, we hope to support multiple keys for different APIs, and the ability to enter your own key.
    key = 'a1078617'

    # For now, this is film titles, later it should be film IDs.
    # This is just to populate the listbox with film titles so it looks good, later we should store the
    # titles somewhere so we're not waiting for years to get the titles when we open the program.
    # But actually use IDs to query the database when we select something in the listbox.
    # Also obviously we'll be able to enter our own...
    films = ['The Matrix', 'The Incredibles', 'Venom']
