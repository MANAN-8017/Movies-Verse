from termcolor import colored
from .utils.movie_cache import *
from django.conf import settings
from django.core.cache import cache
from ..services.omdb_movie_service import *
from ..services.tmdb_movie_service import *

OMDB_API_KEY = settings.OMDB_API_KEY
BASE_OMDB = "http://www.omdbapi.com/"

TMDB_API_KEY = settings.TMDB_API_KEY
BASE_TMDB = "https://api.themoviedb.org/3"
    
def get_movies(imdb_id):

    cache_key = f"movie_{imdb_id}"
    cached_movie = cache.get(cache_key)

    if cached_movie and cached_movie.get("actors") and cached_movie.get("backdrop"):
        print(colored(f"{cached_movie.get('title')} is fully cached (OMDB + TMDB)", "green"))
        return cached_movie

    movie = None

    if cached_movie:
        print(colored(f"Using cached OMDB data for {cached_movie.get('title')}", "blue"))
        movie = cached_movie
    else:
        print(f"Fetching data for {imdb_id} from OMDB...")
        movie = fetch_from_omdb(imdb_id)

        if movie:
            print(colored(f"Successfully fetched {movie.get('title')} from OMDB", "blue"))
        else:
            print(colored("OMDB failed. Trying TMDB only...", "red"))

    print(colored("Trying TMDB for extra data...", "yellow"))

    tmdb_movie = fetch_from_tmdb(imdb_id)

    if tmdb_movie:
        movie = tmdb_movie
        print(colored(f"TMDB enrichment successful for {movie.get('title')}", "green"))
    else:
        print(colored("TMDB did not return additional data", "red"))

    if movie:
        cache.set(cache_key, movie, timeout=60*60*24)

    return movie

def search_movies(movie_name):

    tmdb_results = search_tmdb_movies(movie_name)
    omdb_results = search_omdb_movies(movie_name)

    return tmdb_results + [
        m for m in omdb_results
        if m["imdb_id"] not in {t["imdb_id"] for t in tmdb_results}
    ]