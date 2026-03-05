from django.shortcuts import redirect, render
import requests

TMDB_API_KEY = "d640e3df64686129c3144ad6b3f247cd"
BASE_TMDB = "https://api.themoviedb.org/3"

OMDB_API_KEY = "5fde9780"
BASE_OMDB = "http://www.omdbapi.com/"

def fetch_from_tmdb_by_id(movie_id):
    try:
        response = requests.get(
            f"{BASE_TMDB}/movie/{movie_id}",
            params={
                "api_key": TMDB_API_KEY,
                "append_to_response": "videos,credits"
            },
            timeout=5
        )

        if response.status_code != 200:
            return None

        movie = response.json()

        # Extract trailer
        trailer = next(
            (
                v.get("key")
                for v in movie.get("videos", {}).get("results", [])
                if v.get("type") == "Trailer" and v.get("site") == "YouTube"
            ),
            None
        )

        # Extract credits
        crew = movie.get("credits", {}).get("crew", [])
        cast = movie.get("credits", {}).get("cast", [])

        movie["Director"] = ", ".join(
            c["name"] for c in crew if c.get("job") == "Director"
        )

        movie["Writer"] = ", ".join(
            c["name"] for c in crew if c.get("job") in ["Writer", "Screenplay"]
        )

        movie["Actors"] = ", ".join(
            c["name"] for c in cast[:5]
        )

        movie["trailer"] = trailer
        movie["source"] = "tmdb"

        return movie

    except requests.RequestException:
        return None
    
def fetch_from_tmdb_by_name(movie_name):
    try:
        search = requests.get(
            f"{BASE_TMDB}/search/movie",
            params={"api_key": TMDB_API_KEY, "query": movie_name},
            timeout=5
        )

        if search.status_code != 200:
            return None

        results = search.json().get("results", [])
        if not results:
            return None

        movie_id = results[0]["id"]

        details = requests.get(
            f"{BASE_TMDB}/movie/{movie_id}",
            params={"api_key": TMDB_API_KEY, "append_to_response": "videos,credits"},
            timeout=5
        )

        if details.status_code != 200:
            return None

        movie = details.json()

        trailer = None
        for v in movie.get("videos", {}).get("results", []):
            if v["type"] == "Trailer" and v["site"] == "YouTube":
                trailer = v["key"]
                break

        release_date = movie.get("release_date")
        year = release_date[:4] if release_date else ""

        return {
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
            "year": year,
            "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None,
            "backdrop": f"https://image.tmdb.org/t/p/original{movie.get('backdrop_path')}" if movie.get("backdrop_path") else None,
            "trailer": trailer,
            "runtime": movie.get("runtime"),
            "rating": movie.get("vote_average"),
            "review_count": movie.get("vote_count"),
            "credits": credits,


            # "genres": movie.get("Genre").split(", ") if movie.get("Genre") else [],
            # "language": movie.get("Language"),
            # "director": movie.get("Director"),
            # "writer": movie.get("Writer"),
            # "director": movie.get("Director").split(", ") if movie.get("Director") else [],
            # "writer": movie.get("Writer").split(", ") if movie.get("Writer") else [],
        }

    except requests.RequestException:
        return None

def fetch_from_omdb_by_id(movie_id):
    try:
        response = requests.get(
            BASE_OMDB,
            params={"apikey": OMDB_API_KEY, "i": movie_id},
            timeout=5
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if data.get("Response") != "True":
            return None

        release_date = data.get("Released")
        year = release_date[-4:] if release_date else ""

        actor = data.get("Actors").split(", ") if data.get("Actors") else []

        print(data.get("Trailer"))
        return {
            "title": data.get("Title"),
            "overview": data.get("Plot"),
            "genres": data.get("Genre").split(", ") if data.get("Genre") else [],
            "release_date": data.get("Released"),
            "year": year,
            "language": data.get("Language"),
            "runtime": data.get("Runtime"),
            "director": data.get("Director"),
            "writer": data.get("Writer"),
            "rating": data.get("imdbRating"),
            "review_count": data.get("imdbVotes"),
            "director": data.get("Director").split(", ") if data.get("Director") else [],
            "writer": data.get("Writer").split(", ") if data.get("Writer") else [],
            "actor": actor,
            "poster": data.get("Poster"),
            "backdrop": None,
            "trailer": data.get("Trailer"),
            "source": "omdb",
        }

    except requests.RequestException:
        return None
    
    
def fetch_from_omdb_by_name(movie_name):
    try:
        response = requests.get(
            BASE_OMDB,
            params={"apikey": OMDB_API_KEY, "t": movie_name},
            timeout=5
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if data.get("Response") != "True":
            return None

        release_date = data.get("Released")
        year = release_date[-4:] if release_date else ""

        actor = data.get("Actors").split(", ") if data.get("Actors") else []

        return {
            "source": "omdb",
            "title": data.get("Title"),
            "overview": data.get("Plot"),
            "genres": data.get("Genre").split(", ") if data.get("Genre") else [],
            "release_date": data.get("Released"),
            "year": year,
            "language": data.get("Language"),
            "runtime": data.get("Runtime"),
            "director": data.get("Director"),
            "writer": data.get("Writer"),
            "rating": data.get("imdbRating"),
            "review_count": data.get("imdbVotes"),
            "director": data.get("Director").split(", ") if data.get("Director") else [],
            "writer": data.get("Writer").split(", ") if data.get("Writer") else [],
            "actor": actor,
            "poster": data.get("Poster"),
            "backdrop": None,
            "trailer": None,
        }

    except requests.RequestException:
        return None

def get_movie_with_fallback(movie_name):

    movie = fetch_from_tmdb_by_name(movie_name)

    if movie:
        return movie

    return fetch_from_omdb_by_name(movie_name)