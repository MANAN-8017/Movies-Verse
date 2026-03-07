from django.shortcuts import render
from MoviesVerse.services.movie_service import *

def index(request):

    featured_movie = get_movies("tt15398776")

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