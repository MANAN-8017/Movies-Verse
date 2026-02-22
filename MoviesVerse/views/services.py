from MoviesVerse.models import ProductionHouse
from MoviesVerse.services.tmdb_services import get_movie_production_houses
import requests
from django.shortcuts import render

TMDB_KEY = "d640e3df64686129c3144ad6b3f247cd"
BASE = "https://api.themoviedb.org/3"


def movie_detail(request, movie_id):

    # movie details
    movie = requests.get(
        f"{BASE}/movie/{movie_id}",
        params={"api_key": TMDB_KEY, "append_to_response": "credits,videos"}
    ).json()

    # trailer
    trailer = None
    for v in movie.get("videos", {}).get("results", []):
        if v["type"] == "Trailer" and v["site"] == "YouTube":
            trailer = v["key"]
            break

    context = {
        "movie": movie,
        "trailer": trailer,
        "poster": "https://image.tmdb.org/t/p/w500" + movie["poster_path"] if movie.get("poster_path") else None,
        "backdrop": "https://image.tmdb.org/t/p/original" + movie["backdrop_path"] if movie.get("backdrop_path") else None,
    }

    return render(request, "movie_detail.html", context)


def save_production_houses(movie_name):
    companies = get_movie_production_houses(movie_name)

    for company in companies:
        ProductionHouse.objects.get_or_create(
            tmdb_id = company["id"],
            defaults={
                "production_house_name": company["name"],
                "origin_country": company["origin_country"],
                "tmdb_logo_path": company["logo_path"]
            }
        )