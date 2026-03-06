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
    extra_movies = [get_movies(i) for i in more_ids]

    context = {
        "featured_movie": featured_movie,
        "trending_movies": trending_movies,
        "popular_movies": popular_movies,
        "extra_movies": extra_movies,
    }

    return render(request, "index.html", context)

def trending(request):

    ids = [
        "tt1825683",   # Black Panther
        "tt1745960",   # Top Gun: Maverick
        "tt6263850",   # Deadpool & Wolverine
        "tt1285016",   # The Social Network (original — no confirmed 2024 version)
        "tt1136617",   # The Killer (2023)
        "tt5592244",   # The Guilty (2021)
        "tt5109286",   # Final Destination: Bloodlines
        "tt16366836",  # Venom: The Last Dance
        "tt5433140",   # Fast X
        "tt22687790",  # A Haunting in Venice
        "tt13452446",  # Damsel
        "tt9663764",   # Aquaman and the Lost Kingdom
        "tt14627658",  # The Conjuring: Last Rites
        "tt2356777",   # Terrifier 3
        "tt26736843",  # Atlas
        "tt13211194",  # Backett (Beckett – correct spelling)
        "tt14627620"   # The Secret Agent
    ]

    movies = [get_movies(i) for i in ids]

    context = {
        "movies": movies,
    }

    return render(request, 'trending.html', context)

def popular(request):

    ids = [
        "tt0468569",  # Batman: The Dark Knight (2008)
        "tt1375666",  # Inception (2010)
        "tt0816692",  # Interstellar (2014)
        "tt4154796",  # Avengers: Endgame (2019)
        "tt15398776", # Oppenheimer (2023)
        "tt0241527",  # Harry Potter and the Sorcerer's Stone (2001)
        # None,         # F1: The Movie (no confirmed IMDb page yet)
        # None,         # Avatar: Fire and Ash (not officially released yet)
        # None,         # Mission: Impossible - The Final Reckoning (unreleased)
        # None,         # Frankenstein (2025 — multiple projects, no confirmed listing)
        # None,         # Nuremberg (2025 — no finalized IMDb entry)
        # None,         # Predator: Badlands (unreleased / no stable IMDb ID yet)
        # None,         # Black Bag (2025 — not finalized listing)
        # None,         # The Tiger (2025 — ambiguous title, no confirmed listing)
        # None,         # Jay Kelly (2025 — no confirmed IMDb entry)
        # None,         # Dracula (2025 — multiple projects, no confirmed ID)
        # None,         # Primate (2025 — no confirmed IMDb page)
        # None          # Jurassic World: Rebirth (2025 — not released yet)
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