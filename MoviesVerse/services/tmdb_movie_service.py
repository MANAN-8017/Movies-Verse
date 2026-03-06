import requests
from .utils.movie_cache import *
from django.core.cache import cache

TMDB_API_KEY = "d640e3df64686129c3144ad6b3f247cd"
BASE_TMDB = "https://api.themoviedb.org/3"

def build_movie_data_tmdb(movie):

    release_date = clean(movie.get("release_date"))
    year = release_date[:4] if release_date else ""

    genres = [g["name"] for g in movie.get("genres", [])]

    cast = []
    for actors in movie.get("credits", {}).get("cast", [])[:12]:
        cast.append({
            "name": actors["name"],
            "character": actors["character"],
            "profile_path": actors["profile_path"]
        })

    crew = movie.get("credits", {}).get("crew", [])
    directors = [c["name"] for c in crew if c.get("job") == "Director"]
    writers = [c["name"] for c in crew if c.get("job") in ["Writer", "Screenplay"]]

    videos = movie.get("videos", {}).get("results", [])

    trailer = None

    for v in videos:
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            trailer = v["key"]
            break

    if not trailer:
        for v in videos:
            if v["site"] == "YouTube":
                trailer = v["key"]
                break

    poster = (
        f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
        if movie.get("poster_path")
        else None
    )

    backdrop = (
        f"https://image.tmdb.org/t/p/original{movie.get('backdrop_path')}"
        if movie.get("backdrop_path")
        else None
    )

    movie_data = {
        "imdb_id": clean(movie.get("imdb_id")),
        "tmdb_id": movie.get("tmdb_id"),
        "title": clean(movie.get("title")),
        "overview": clean(movie.get("overview")),
        "genres": genres,
        "release_date": release_date,
        "year": year,
        "runtime": clean(movie.get("runtime")),
        "rating": clean(movie.get("vote_average")),
        "review_count": clean(movie.get("vote_count")),
        "directors": directors,
        "writers": writers,
        "actors": cast,
        "poster": poster,
        "backdrop": backdrop,
        "trailer": trailer,
        "source": "tmdb"
    }

    return movie_data
    
def fetch_from_tmdb(imdb_id):

    cache_key = f"movie_{imdb_id}"
    cached_movie = cache.get(cache_key)

    try:
        response = requests.get(
            f"{BASE_TMDB}/find/{imdb_id}",
            params={
                "api_key": TMDB_API_KEY,
                "external_source": "imdb_id"
            },
            timeout=5
        )

        if response.status_code != 200:
            return cached_movie

        data = response.json()

        results = data.get("movie_results", [])
        if not results:
            return cached_movie

        movie_id = results[0]["id"]

        details = requests.get(
            f"{BASE_TMDB}/movie/{movie_id}",
            params={
                "api_key": TMDB_API_KEY,
                "append_to_response": "videos,credits"
            },
            timeout=5
        )

        if details.status_code != 200:
            return cached_movie

        movie = details.json()

        movie["tmdb_id"] = movie_id

        tmdb_data = build_movie_data_tmdb(movie)
        merged_movie = merge_movie_data(cached_movie, tmdb_data)

        cache.set(cache_key, merged_movie, timeout=60*60*24)

        return merged_movie

    except requests.RequestException:
        return cached_movie
    
def search_tmdb_movies(movie_name):
    try:
        response = requests.get(
            f"{BASE_TMDB}/search/movie",
            params={"api_key": TMDB_API_KEY, "query": movie_name},
            timeout=5
        )

        if response.status_code != 200:
            return []

        results = response.json().get("results", [])

        return [
            {
                "title": m.get("title"),
                "year": m.get("release_date", "")[:4],
                "poster": f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}" if m.get("poster_path") else None,
                "tmdb_id": m.get("id"),
                "imdb_id": None,
                "source": "tmdb"
            }
            for m in results[:10]
        ]

    except requests.RequestException:
        return []