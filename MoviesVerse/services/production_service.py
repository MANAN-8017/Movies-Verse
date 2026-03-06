
import requests
from django.core.cache import cache
from MoviesVerse.services.tmdb_movie_service import BASE_TMDB, TMDB_API_KEY, merge_movie_data

def fetch_movies_by_company(tmdb_company_id):
    try:
        response = requests.get(
            f"{BASE_TMDB}/discover/movie",
            params={
                "api_key": TMDB_API_KEY,
                "with_companies": tmdb_company_id,
                "sort_by": "release_date.desc"
            },
            timeout=5
        )

        if response.status_code != 200:
            return []

        return response.json().get("results", [])

    except requests.RequestException:
        return []