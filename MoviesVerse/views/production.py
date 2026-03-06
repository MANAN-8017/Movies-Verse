from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from MoviesVerse.models import Favourite, ProductionHouse
import requests
from MoviesVerse.services.production_service import fetch_movies_by_company
from MoviesVerse.services.tmdb_movie_service import BASE_TMDB, TMDB_API_KEY, merge_movie_data
from MoviesVerse.models import Movie, Watchlist, Favourite

def production_house_dashboard(request):
    ph_id = request.session.get('production_house_id')
    if not ph_id:
        return redirect('sign_in')

    production_house = ProductionHouse.objects.get(id=ph_id)

    movies = []
    if production_house.tmdb_company_id:
        movies = fetch_movies_by_company(production_house.tmdb_company_id)

    return render(request, 'production_house/production_house_dashboard.html', {
        'production': production_house,
        'movies': movies,
    })

def production_analytics(request):
    ph_id = request.session.get('production_house_id')
    if not ph_id:
        return redirect('sign_in')

    production_house = ProductionHouse.objects.get(id=ph_id)

    # movies from TMDB
    tmdb_movies = []
    if production_house.tmdb_company_id:
        tmdb_movies = fetch_movies_by_company(production_house.tmdb_company_id)

    # Top 5 
    top_5_movies = sorted(
        tmdb_movies,
        key=lambda m: m.get('popularity', 0),
        reverse=True
    )[:5]

    # Total
    total_films = len(tmdb_movies)

    # tmdb rating
    rated = [m['vote_average'] for m in tmdb_movies if m.get('vote_average')]
    avg_rating = round(sum(rated) / len(rated), 1) if rated else None

    # Get TMDB IDs to find matching local DB movies
    tmdb_ids = [m["id"] for m in tmdb_movies if m.get("id")]
    local_movies = Movie.objects.filter(tmdb_id__in=tmdb_ids)

    # Watchlist and favourite counts from local DB
    total_watchlists = Watchlist.objects.filter(movie__in=local_movies).count()
    total_favourites = Favourite.objects.filter(movie__in=local_movies).count()

    return render(request, 'production_house/production_analytics.html', {
        'production': production_house,
        'movies': top_5_movies,
        'total_films': total_films,
        'avg_rating': avg_rating,
        'total_watchlists': total_watchlists,
        'total_favourites': total_favourites,
    })


def add_promotion(request):
    ph_id = request.session.get('production_house_id')
    if not ph_id:
        return redirect('sign_in')
    
    production_house = ProductionHouse.objects.get(id=ph_id)

    if request.method == 'POST':
        # handle form submission later
        pass

    return render(request, 'production_house/add_promotion.html', {
        'production': production_house,
        'movies': [],
        'promotions': [],
    })