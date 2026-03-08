from datetime import date, datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from MoviesVerse.models import Favourite, ProductionHouse, Promotion
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
        
    total_films = len(movies)
    
    rated = [m['vote_average'] for m in movies if m.get('vote_average')]
    avg_rating = round(sum(rated) / len(rated), 1) if rated else None
    
    today = date.today()
    upcoming_count = 0  
    for movie in movies:
        realese_date_str = movie.get('release_date')
        if realese_date_str and realese_date_str > str(today) :
            movie['status'] = 'upcoming'
            upcoming_count += 1
        else:
            movie['status'] = 'released'

    return render(request, 'production_house/production_house_dashboard.html', {
        'production': production_house,
        'movies': movies,
        'avg_rating': avg_rating,
        'total_films': total_films,
        'upcoming_count': upcoming_count,
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
        title        = request.POST.get('title', '').strip()
        description  = request.POST.get('description', '').strip()
        release_date = request.POST.get('release_date') or None
        language     = request.POST.get('language', 'en')
        tags         = request.POST.get('tags', '').strip()
        promo_type   = request.POST.get('promo_type', 'trailer')
        media_file   = request.FILES.get('media_file')
        thumbnail    = request.FILES.get('thumbnail')

        Promotion.objects.create(
            production_house=production_house,
            title=title,
            description=description,
            release_date=release_date,
            language=language,
            tags=tags,
            promo_type=promo_type,
            media_file=media_file,
            thumbnail=thumbnail,
        )
        return redirect('my_promotions')

    return render(request, 'production_house/add_promotion.html', {
        'production': production_house,
    })
    
    
def my_promotions(request):
    ph_id = request.session.get('production_house_id')
    if not ph_id:
        return redirect('sign_in')

    production_house = ProductionHouse.objects.get(id=ph_id)
    promotions = Promotion.objects.filter(production_house=production_house)

    return render(request, 'production_house/my_promotions.html', {
        'production': production_house,
        'promotions': promotions,
    })
    

def delete_promotion(request, promo_id):
    ph_id = request.session.get('production_house_id')
    if not ph_id:
        return redirect('sign_in')

    promotion = Promotion.objects.get(id=promo_id)

    if promotion.production_house.id != ph_id:
        return redirect('my_promotions')

    promotion.delete()
    return redirect('my_promotions')


def edit_promotion(request, promo_id):
    ph_id = request.session.get('production_house_id')
    if not ph_id:
        return redirect('sign_in')

    promotion = Promotion.objects.get(id=promo_id)

    if promotion.production_house.id != ph_id:
        return redirect('my_promotions')

    if request.method == 'POST':
        promotion.title       = request.POST.get('title', '').strip()
        promotion.description = request.POST.get('description', '').strip()
        promotion.release_date = request.POST.get('release_date') or None
        promotion.language    = request.POST.get('language', 'en')
        promotion.tags        = request.POST.get('tags', '').strip()
        promotion.promo_type  = request.POST.get('promo_type', 'trailer')

        if request.FILES.get('media_file'):
            promotion.media_file = request.FILES['media_file']
        if request.FILES.get('thumbnail'):
            promotion.thumbnail = request.FILES['thumbnail']

        promotion.save()
        return redirect('my_promotions')

    return render(request, 'production_house/edit_promotion.html', {
        'production': promotion.production_house,
        'promo': promotion,
    })
    
    
def production_settings(request):
    ph_id = request.session.get('production_house_id')
    if not ph_id:
        return redirect('sign_in')

    production_house = ProductionHouse.objects.get(id=ph_id)
    error = None
    success = None

    if request.method == 'POST':
        action = request.POST.get('action')

        # ── Basic Info ──
        if action == 'basic_info':
            production_house.name = request.POST.get('name', '').strip()
            production_house.headquarters = request.POST.get('headquarters', '').strip()
            production_house.founded_year = request.POST.get('founded_year') or None
            production_house.contact_number = request.POST.get('contact_number', '').strip()
            production_house.save()
            success = 'Basic info updated successfully.'

        # ── Logo ──
        elif action == 'logo':
            if request.FILES.get('logo'):
                production_house.logo = request.FILES['logo']
                production_house.save()
                success = 'Logo updated successfully.'
            else:
                error = 'Please select a logo file.'

        # ── Password ──
        elif action == 'password':
            current_password  = request.POST.get('current_password')
            new_password      = request.POST.get('new_password')
            confirm_password  = request.POST.get('confirm_password')

            if not django_check_password(current_password, production_house.password):
                error = 'Current password is incorrect.'
            elif new_password != confirm_password:
                error = 'New passwords do not match.'
            elif len(new_password) < 6:
                error = 'New password must be at least 6 characters.'
            else:
                production_house.password = make_password(new_password)
                production_house.save()
                success = 'Password changed successfully.'

    return render(request, 'production_house/production_setting.html', {
        'production': production_house,
        'error': error,
        'success': success,
    })