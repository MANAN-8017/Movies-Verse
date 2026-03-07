
import requests
from django.conf import settings

TMDB_API_KEY = settings.TMDB_API_KEY
BASE_TMDB = "https://api.themoviedb.org/3"

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