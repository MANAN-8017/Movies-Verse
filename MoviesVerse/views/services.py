from pprint import pprint
from MoviesVerse.models import *
from django.shortcuts import render
from django.http import HttpResponse
from MoviesVerse.services.movie_service import *

def search_movies(request):
    query = request.GET.get("q", "").strip()
    results = search_movies(query)

    if results:
        return render(request, "search.html", {"results": results})

    return HttpResponse("No movies found", status=404)

def movie_detail(request, imdb_id):
    movie = get_movies(imdb_id)
    
    if movie:
        return render(request, "movie_detail.html", {"movie": movie})

    return HttpResponse("Movie not found", status=404)