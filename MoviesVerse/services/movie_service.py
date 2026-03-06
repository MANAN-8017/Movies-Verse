from termcolor import colored
from .utils.movie_cache import *
from django.core.cache import cache
from ..services.omdb_movie_service import *
from ..services.tmdb_movie_service import *

OMDB_API_KEY = "5fde9780"
BASE_OMDB = "http://www.omdbapi.com/"

TMDB_API_KEY = "d640e3df64686129c3144ad6b3f247cd"
BASE_TMDB = "https://api.themoviedb.org/3"
    
def get_movies(imdb_id):

    cache_key = f"movie_{imdb_id}"
    cached_movie = cache.get(cache_key)

    if cached_movie:
        if cached_movie.get("actors") and cached_movie.get("backdrop"):
            print(colored(f"{cached_movie.get('title')} is already fully cached including TMDB data", 'green'))
            return cached_movie

    print(f"Fetching for {imdb_id} from OMDB...")
    movie = fetch_from_omdb(imdb_id)

    if movie:
        print(f"Trying TMDB for {movie.get('title')}'s extra data...")
    else:
        print(colored("Couldn't fetch data from OMDB!", 'red'))
        print("Fetching data from TMDB...")
    
    movie = fetch_from_tmdb(imdb_id)

    if movie and movie.get("actors"):
        print(colored(f"TMDB data successfully merged for {movie.get('title')}", 'green'))
    else:
        if movie: 
            print(colored(f"TMDB did NOT return extra data for {movie.get('title')}", 'red'))
        else:
            print(colored(f"Movie not found using id: {imdb_id}", 'red'))

    return movie

def search_movies(movie_name):

    tmdb_results = search_tmdb_movies(movie_name)
    omdb_results = search_omdb_movies(movie_name)

    return tmdb_results + [
        m for m in omdb_results
        if m["imdb_id"] not in {t["imdb_id"] for t in tmdb_results}
    ]