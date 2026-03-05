from django.http import HttpResponse

from MoviesVerse.models import *
from MoviesVerse.services.movie_service import *
from django.shortcuts import render

TMDB_KEY = "d640e3df64686129c3144ad6b3f247cd"
BASE = "https://api.themoviedb.org/3"

def search_movies(request):
    query = request.GET.get("q", "").strip()
    results = fetch_from_omdb_by_id(query)

    if not results:
        results = fetch_from_tmdb_by_name(query)

    return render(request, "search.html", {"results": results})

def movie_detail(request, movie_id):
    movie = fetch_from_omdb_by_id(movie_id)

    if movie:
        return render(request, "movie_detail.html", {"movie": movie})

    # Trying TMDb
    movie_name = movie.get("title")
    print(f"Movie not found in OMDb, trying TMDb with name: {movie_name}")
    movie = fetch_from_tmdb_by_name(movie_name)

    if movie:
        return render(request, "movie_detail_tmdb.html", {"movie": movie})

    return HttpResponse("Movie not found", status=404)