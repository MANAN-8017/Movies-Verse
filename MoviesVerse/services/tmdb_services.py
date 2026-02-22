import requests

TMDB_API_KEY = "YOUR_KEY"
BASE_URL = "https://api.themoviedb.org/3"

def get_movie_production_houses(movie_name):
    # 1 search movie
    search = requests.get(
        f"{BASE_URL}/search/movie",
        params={"api_key": TMDB_API_KEY, "query": movie_name}
    ).json()

    if not search["results"]:
        return []

    movie_id = search["results"][0]["id"]

    # 2 movie details
    details = requests.get(
        f"{BASE_URL}/movie/{movie_id}",
        params={"api_key": TMDB_API_KEY}
    ).json()

    return details.get("production_companies", [])
