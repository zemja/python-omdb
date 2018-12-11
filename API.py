import math
import urllib
import json

# For convenience. Turn `thing` into None if it's 'N/A'
def na_none(thing):
    return thing if thing != 'N/A' else None

class FilmInfo:
    # For stupid reasons (time) these are all strings instead of a nice format. Please just pass
    # them as strings.
    # Except `rating`, which is an int from 1-5.
    # `poster` should be the URL of a poster on the Internet (direct link to image of course) or
    # None if there isn't one.
    def __init__(self, title, genre, released, runtime, director, rating, plot, actors, poster):
        self.title    = title
        self.genre    = genre
        self.released = released
        self.runtime  = runtime
        self.director = director
        self.rating   = rating
        self.plot     = plot
        self.actors   = actors
        self.poster   = poster

class API:
    def __init__(self, key):
        raise NotImplementedError('BUG: `API` method `__init__()` wasn\'t overloaded.')

    # Should return an array that goes [['ID', 'Title', 'Released'], ['ID', 'Title', 'Released'] ...etc... ]
    # Might throw some exceptions, just catch `Exception` instead because it's easier, and make a
    # donation to some charity for programmers with PTSD to make up for it.
    def search(self, title):
        raise NotImplementedError('BUG: `API` method `search()` wasn\'t overloaded.')

    # Should return a `FilmInfo`.
    # Same exception dealio as `search()`.
    # `ID` should be the IMDb ID. Confusing I know, because `search()` gives back whatever ID that
    # API uses.
    def get(self, ID):
        raise NotImplementedError('BUG: `API` method `get()` wasn\'t overloaded.')

    # If your API doesn't use IMDb IDs, this method should get the imdb ID of a film from the ID
    # that it does use. Or None if it can't.
    def imdb_id(self, ID):
        raise NotImplementedError('BUG: `API` method `imdb_id()` wasn\'t overloaded.')

class OMDB(API):
    def __init__(self, key):
        self.key = key

    def search(self, title):
        response = json.loads(urllib.request.urlopen(f'http://www.omdbapi.com/?apikey={self.key}&s={urllib.parse.quote_plus(title)}').read().decode('utf-8'))

        if response['Response'] == 'False':
            raise Exception(response['Error'])

        results = []

        for result in response['Search']:
            results.append([result['imdbID'], result['Title'], result['Year']])

        return results

    def get(self, ID):
        response = json.loads(urllib.request.urlopen(f'http://www.omdbapi.com/?apikey={self.key}&i={ID}&plot=full').read().decode('utf-8'))

        if response['Response'] == 'False':
            raise Exception(response['Error'])

        info = FilmInfo (
            title    = na_none(response['Title']),
            genre    = na_none(response['Genre']),
            released = na_none(response['Released']),
            runtime  = na_none(response['Runtime']),
            director = na_none(response['Director']),
            rating   = na_none(response['imdbRating']),
            plot     = na_none(response['Plot']),
            actors   = na_none(response['Actors']),
            poster   = na_none(response['Poster'])
        )

        if info.rating is not None:
            info.rating = math.ceil(float(info.rating) / 2)

        return info

    def imdb_id(self, ID):
        return ID

class TMDB(API):
    def __init__(self, key):
        self.key = key

    def search(self, title):
        response = json.loads(urllib.request.urlopen(f'https://api.themoviedb.org/3/search/movie?api_key={self.key}&query={urllib.parse.quote_plus(title)}').read().decode('utf-8'))

        if 'status_code' in response:
            raise Exception(response['status_message'])

        if response['total_results'] == 0:
            raise Exception('No results found')

        results = []

        for result in response['results']:
            results.append([result['id'], result['title'], result['release_date']])

        return results

    def get(self, ID):
        # First request gets basic movie info (including TMDb ID) from the IMDb ID.
        response = json.loads(urllib.request.urlopen(f'https://api.themoviedb.org/3/find/{ID}?api_key={self.key}&external_source=imdb_id').read().decode('utf-8'))

        if 'status_code' in response:
            raise Exception(response['status_message'])

        if not response['movie_results']:
            raise Exception(f'Movie with IMDb ID {ID} not found')

        # Second request gets all the movie info from the TMDb ID. Just get the first movie that resulted from that IMDb ID.
        response = json.loads(urllib.request.urlopen(f"https://api.themoviedb.org/3/movie/{response['movie_results'][0]['id']}?api_key={self.key}&append_to_response=credits").read().decode('utf-8'))

        if 'status_code' in response:
            raise Exception(response['status_message'])

        info = FilmInfo (
            title    = response['title'],
            genre    = response['genres'],
            released = response['release_date'],
            runtime  = f"{response['runtime']} min" if response['runtime'] is not None else response['runtime'],
            director = '',
            rating   = response['vote_average'],
            plot     = response['overview'],
            actors   = '',
            poster   = f"https://image.tmdb.org/t/p/w500{response['poster_path']}" if response['poster_path'] is not None else response['poster_path']
        )

        # Concatenate genre names into a comma-separated string
        if info.genre and info.genre is not None:
            genres = info.genre[0]['name']
            for genre in info.genre[1:]:
                genres += f", {genre['name']}"
            info.genre = genres

        if 'credits' in response and response['credits'] is not None and 'crew' in response['credits'] and response['credits']['crew'] is not None:
            # Get everyone's name who has job 'Director' from the credits into a list
            directors = []
            for credit in response['credits']['crew']:
                if credit['job'] == 'Director':
                    directors.append(credit['name'])
            # Now concatenate them all into a comma-separated string
            if directors:
                info.director = directors[0]
                for director in directors[1:]:
                    info.director += f', {director}'

        if info.director == '':
            info.director = None

        # If there were any votes, get the rating as an integer 1-5 if there is one, otherwise it's None
        if response['vote_count'] == 0:
            info.rating = None
        else:
            info.rating = math.ceil(response['vote_average'] / 2) if response['vote_average'] is not None else response['vote_average']

        # Similar dealio to director(s), but get up to the first four actor's names
        if 'credits' in response and response['credits'] is not None and 'cast' in response['credits'] and response['credits']['cast'] is not None and response['credits']['cast']:
            info.actors = response['credits']['cast'][0]['name']
            for actor in response['credits']['cast'][1:min(4, len(response['credits']['cast']))]:
                info.actors += f", {actor['name']}"

        if info.actors == '':
            info.actors = None


        return info

    def imdb_id(self, ID):
        response = json.loads(urllib.request.urlopen(f'https://api.themoviedb.org/3/movie/{ID}/external_ids?api_key={self.key}').read().decode('utf-8'))

        if 'status_code' in response:
            raise Exception(response['status_message'])

        return response['imdb_id']
