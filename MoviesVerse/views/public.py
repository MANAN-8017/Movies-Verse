from django.shortcuts import render
from MoviesVerse.services.movie_service import *
from ..models import Watchlist, Movie, Like, Watched
from MoviesVerse.models import Movie, Watchlist
from MoviesVerse.services.movie_service import get_movies


def index(request):

    featured_movie = get_movies("tt15398776")

    from ..models import Watchlist

    is_in_watchlist = False

    if request.user.is_authenticated and featured_movie:
        imdb_id = featured_movie.get("imdb_id") or featured_movie.get("imdbID")

        is_in_watchlist = Watchlist.objects.filter(
            user=request.user,
            movie__omdb_id=imdb_id
        ).exists()

    trending_ids = [
        "tt0120338",  # Titanic
        "tt6263850",  # Deadpool & Wolverine
        "tt1745960",  # Top Gun Maverick
        "tt9619824",  # Final Destination: Bloodlines
        "tt1285016",  # The Social Network
        "tt1825683",  # Black Panther

    ]

    popular_ids = [
        "tt1757678",  # Avatar: Fire and Ash
        "tt16311594", # F1: The Movie
        "tt0468569",  # Batman: The Dark Knight
        "tt0816692",  # Interstellar
        "tt4154796",  # Avengers: Endgame
        "tt9603212",  # Mission Impossible: The Final Reckoning
    ]

    more_ids = [
        "tt9362722",  # Spider-Man: Across the Spider-Verse
        "tt7286456",  # Joker
        "tt1375666",  # Inception
        "tt0133093",  # The Matrix
        "tt0109830",  # Forrest Gump
        "tt0120737",  # The Lord of the Rings: The Fellowship of the Ring
        "tt0111161",  # Shawshank
    ]

    trending_movies = [get_movies(i) for i in trending_ids]
    popular_movies = [get_movies(i) for i in popular_ids]
    # extra_movies = [get_movies(i) for i in more_ids]

    context = {
        "featured_movie": featured_movie,
        "trending_movies": trending_movies,
        "popular_movies": popular_movies,
        # "extra_movies": extra_movies,
        "is_in_watchlist": is_in_watchlist
    }

    return render(request, "index.html", context)

def trending(request):

    ids = [
        "tt1825683",   # Black Panther
        "tt1745960",   # Top Gun: Maverick
        "tt6263850",   # Deadpool & Wolverine
        "tt1285016",   # The Social Network
        "tt1136617",   # The Killer
        "tt9421570",   # The Guilty
        "tt9619824",   # Final Destination: Bloodlines
        "tt16366836",  # Venom: The Last Dance
        "tt5433140",   # Fast X
        "tt22687790",  # A Haunting in Venice
        "tt13452446",  # Damsel
        "tt9663764",   # Aquaman and the Lost Kingdom
        "tt22898462",  # The Conjuring: Last Rites
        "tt26736843",  # Atlas
        "tt10230994",  # Beckett
        "tt27847051"   # The Secret Agent
    ]

    movies = [get_movies(i) for i in ids]

    context = {
        "movies": movies,
    }

    return render(request, 'trending.html', context)

def popular(request):

    ids = [
        "tt0468569",  # Batman: The Dark Knight
        "tt1375666",  # Inception
        "tt0816692",  # Interstellar
        "tt4154796",  # Avengers: Endgame
        "tt15398776", # Oppenheimer
        "tt0241527",  # Harry Potter and the Sorcerer's Stone
        "tt16311594", # F1: The Movie
        "tt1757678",  # Avatar: Fire and Ash
        "tt9603208",  # Mission: Impossible - The Final Reckoning
        "tt1312221",  # Frankenstein
        "tt29567915", # Nuremberg
        "tt31227572", # Predator: Badlands
        "tt30988739", # Black Bag
        "tt30446847", # Jay Kelly
        "tt31434030", # Dracula
        "tt33028778", # Primate
        "tt31036941"  # Jurassic World: Rebirth
    ]

    movies = [get_movies(i) for i in ids]

    context = {
        "movies": movies,
    }

    return render(request, 'popular.html', context)

def upcoming(request):
    return render(request, 'upcoming.html')

def help(request):
    return render(request, 'help.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')


def movie_detail(request, imdb_id):

    # Step 1: check if movie already exists in DB
    movie = Movie.objects.filter(omdb_id=imdb_id).first()

    # Step 2: if not found → fetch from API and save
    if not movie:
        data = get_movies(imdb_id)

        movie = Movie.objects.create(
            omdb_id = imdb_id,
            tmdb_id = data.get("tmdb_id") or 0,
            title = data.get("title"),
            poster = data.get("poster"),
            release_year = data.get("year"),
            runtime = int(str(data.get("runtime","0")).split()[0]),
            genres = ", ".join(data.get("genres", [])) if isinstance(data.get("genres"), list) else data.get("genres"),
            overview = data.get("overview"),
            director = ", ".join(data.get("directors", [])) if isinstance(data.get("directors"), list) else data.get("director"),
            origin_country = data.get("language")
        )

    # Step 3: check user status
    is_watchlist = False
    is_liked = False
    is_watched = False

    if request.user.is_authenticated:

        is_watchlist = Watchlist.objects.filter(
            user=request.user,
            movie=movie
        ).exists()

        is_liked = Like.objects.filter(
            user=request.user,
            movie=movie
        ).exists()

        is_watched = Watched.objects.filter(
            user=request.user,
            movie=movie
        ).exists()

    context = {
        "movie": movie,
        "is_in_watchlist": is_watchlist,
        "is_liked": is_liked,
        "is_watched": is_watched
    }

    return render(request, "movie_detail.html", context)