import time
import requests
from django.conf import settings
from django.core.cache import cache

TMDB_API_KEY = settings.TMDB_API_KEY
BASE_TMDB = "https://api.themoviedb.org/3"

def fetch_movies_by_company(tmdb_company_id):
    cache_key = f"company_movies_{tmdb_company_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    for attempt in range(3):
        try:
            response = requests.get(
                f"{BASE_TMDB}/discover/movie",
                params={
                    "api_key":        TMDB_API_KEY,
                    "with_companies": tmdb_company_id,
                    "sort_by":        "release_date.desc"
                },
                timeout=5
            )

            if response.status_code != 200:
                if attempt < 2:
                    time.sleep(1)
                continue

            movies = response.json().get("results", [])
            cache.set(cache_key, movies)
            return movies

        except requests.RequestException:
            print(f"Attempt {attempt+1} to fetch movies for company {tmdb_company_id} failed.")
            if attempt < 2:
                time.sleep(1)

    return []