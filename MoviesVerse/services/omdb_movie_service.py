import requests
from .utils.movie_cache import *
from django.conf import settings
from django.core.cache import cache

OMDB_API_KEY = settings.OMDB_API_KEY
BASE_OMDB = "http://www.omdbapi.com/"

def build_movie_data_omdb(data):

    genre = clean(data.get("Genre"))
    genre = genre.split(", ") if genre else []

    directors = clean(data.get("Director"))
    directors = directors.split(", ") if directors else []

    writers = clean(data.get("Writer"))
    writers = writers.split(", ") if writers else []

    release_date = clean(data.get("Released"))
    year = release_date[-4:] if release_date else ""

    review_count = clean(data.get("imdbVotes", "0").replace(",", ""))
    review_count = int(review_count) if review_count and review_count.isdigit() else 0

    movie_data = {
        "imdb_id": clean(data.get("imdbID")),
        "title": clean(data.get("Title")),
        "overview": clean(data.get("Plot")),
        "genres": genre,
        "release_date": release_date,
        "year": year,
        "language": clean(data.get("Language")),
        "runtime": clean(data.get("Runtime")),
        "rating": clean(data.get("imdbRating")),
        "review_count": review_count,
        "directors": directors,
        "writers": writers,
        "poster": clean(data.get("Poster")),
        "source": "omdb"
    }

    return movie_data

def fetch_from_omdb(imdb_id):

    cache_key = f"movie_{imdb_id}"
    cached_movie = cache.get(cache_key)

    try:
        response = requests.get(
            BASE_OMDB,
            params={"apikey": OMDB_API_KEY, "i": imdb_id},
            timeout=5
        )

        if response.status_code != 200:
            return cached_movie

        data = response.json()

        if data.get("Response") != "True":
            return cached_movie

        movie = build_movie_data_omdb(data)
        merged_movie = merge_movie_data(cached_movie, movie)
        
        return merged_movie

    except requests.RequestException:
        return cached_movie

def search_omdb_movies(movie_name):
    try:
        response = requests.get(
            BASE_OMDB,
            params={"apikey": OMDB_API_KEY, "s": movie_name},
            timeout=5
        )

        if response.status_code != 200:
            return []

        data = response.json()

        if data.get("Response") != "True":
            return []

        return [
            {
                "title": m.get("Title"),
                "year": m.get("Year"),
                "poster": clean(m.get("Poster")),
                "imdb_id": m.get("imdbID"),
                "source": "omdb"
            }
            for m in data.get("Search", [])[:10]
        ]

    except requests.RequestException:
        return []