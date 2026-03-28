from ..models import *
from django.db.models import Sum
from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from MoviesVerse.services.movie_service import get_movies

User = get_user_model()
@login_required
def favourite(request):
    likes_qs = Like.objects.filter(user=request.user).select_related("movie")
    
    context = {
        "likes": [w.movie for w in likes_qs]
    }
    return render(request, 'user/favourite.html', context)

@login_required
def profile(request):

    likes_qs = Like.objects.filter(user=request.user)
    likes_preview = likes_qs[:5]
    print(likes_qs, "liked movies found for user:", request.user.username)

    watched_qs = Watched.objects.filter(user=request.user).select_related("movie")
    watched_preview = watched_qs[:5]

    watchlist_qs = Watchlist.objects.filter(user=request.user).select_related("movie")
    watchlist_preview = watchlist_qs[:5]

    ratings_qs = Rating.objects.filter(user=request.user)
    comments_qs = Comment.objects.filter(user=request.user)
    search_qs = SearchHistory.objects.filter(user=request.user)

    total_runtime = watched_qs.aggregate(total=Sum("movie__runtime"))["total"] or 0

    minutes = total_runtime
    hours = minutes // 60
    minutes = minutes % 60

    days = hours // 24
    hours = hours % 24

    months = days // 30
    days = days % 30

    years = months // 12
    months = months % 12

    context = {
        "watchlist_count": watchlist_qs.count(),
        "total_watched": watched_qs.count(),
        "ratings_count": ratings_qs.count(),
        "comments_count": comments_qs.count(),
        "likes_count": likes_qs.count(),

        "hours": hours,
        "days": days,
        "months": months,
        "years": years,

        "liked_movies": [l.movie for l in likes_preview],
        "watched_movies": [w.movie for w in watched_preview],
        "watchlist_movies": [w.movie for w in watchlist_preview],
        "rated_movies": ratings_qs,
        "user_comments": comments_qs,
        "search_history": search_qs,
    }

    return render(request, "user/profile.html", context)

from datetime import datetime

def get_or_create_movie(imdb_id):

    cache_key = f"movie_model_{imdb_id}"
    movie = cache.get(cache_key)

    if movie:
        return movie

    movie = Movie.objects.filter(omdb_id=imdb_id).first()

    if movie:
        cache.set(cache_key, movie, 60 * 60 * 24)
        return movie

    data = get_movies(imdb_id)

    if not data:
        return None

    runtime_raw = data.get("runtime")

    try:
        runtime = int(str(runtime_raw).split()[0])
    except (ValueError, TypeError):
        runtime = 0

    release_date = data.get("release_date")

    movie = Movie.objects.create(
        omdb_id=imdb_id,
        tmdb_id=data.get("tmdb_id"),
        title=data.get("title") or "Unknown",
        poster=data.get("poster") or "",
        release_date=release_date,
        runtime=runtime,
        genres=", ".join(data.get("genres", [])),
        overview=data.get("overview") or "",
        director=", ".join(data.get("directors", [])),
        origin_country=data.get("language") or ""
    )

    cache.set(cache_key, movie, 60 * 60 * 24)

    return movie

@login_required
def toggle_like(request, imdb_id):

    movie = get_or_create_movie(imdb_id)
    
    print("Movie fetched for like toggle:", movie)

    if not movie:
        return JsonResponse({"status": "error"}, status=400)

    like = Like.objects.filter(user=request.user, movie=movie)

    if like.exists():
        like.delete()
        status = "removed"
    else:
        Like.objects.create(user=request.user, movie=movie)
        status = "added"

    return JsonResponse({"status": status})

@login_required
def toggle_watched(request, imdb_id):

    movie = get_or_create_movie(imdb_id)

    if not movie:
        return JsonResponse({"status": "error"}, status=400)

    watched = Watched.objects.filter(user=request.user, movie=movie)

    if watched.exists():
        watched.delete()
        status = "removed"
    else:
        Watched.objects.create(user=request.user, movie=movie)
        status = "added"

    return JsonResponse({"status": status})

@login_required
def toggle_watchlist(request, imdb_id):

    movie = get_or_create_movie(imdb_id)

    if not movie:
        return JsonResponse({"status": "error"}, status=400)

    watch = Watchlist.objects.filter(user=request.user, movie=movie)

    if watch.exists():
        watch.delete()
        status = "removed"
    else:
        Watchlist.objects.create(user=request.user, movie=movie)
        status = "added"

    count = Watchlist.objects.filter(user=request.user).count()

    return JsonResponse({
        "status": status,
        "count": count
    })

@login_required
def settings_page(request):

    if request.method == "POST":
        profile, created = Profile.objects.get_or_create(user=request.user)

        # Profile Picture
        if "update-profile_pic" in request.POST:
            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]
                if not profile.profile_pic.name.endswith(('.jpg', '.jpeg', '.png')):
                    messages.error(request, "Invalid file type. Please upload a JPG, JPEG, or PNG file.")
                elif profile.profile_pic.size > 5 * 1024 * 1024:
                    messages.error(request, "File size exceeds the 5MB limit.")
                else:
                    profile.save()
                    messages.success(request, "Profile picture updated successfully.")

        # Username
        if "update-username" in request.POST:
            if request.POST.get("new_username"):
                new_username = request.POST.get("new_username")
                if not User.objects.filter(username__iexact=new_username).exclude(id=request.user.id).exists():
                    if not request.user.check_password(request.POST.get("password")):
                        messages.error(request, "Current password is incorrect.")
                    else:
                        print("New Username:", new_username)
                        request.user.username = new_username
                        request.user.save()
                        messages.success(request, "Username updated successfully.")
                else:
                    messages.error(request, "Username already exists.")

        # Email
        if "update-email" in request.POST:
            if request.POST.get("new_email"):
                new_email = request.POST.get("new_email")
                if not User.objects.filter(email__iexact=new_email).exclude(id=request.user.id).exists():
                    if not request.user.check_password(request.POST.get("password")):
                        messages.error(request, "Current password is incorrect.")
                        return redirect("settings")
                    else:
                        request.user.email = new_email
                        request.user.save()
                        messages.success(request, "Email updated successfully.")
                else:
                    messages.error(request, "Email already exists.")

        # Display Name
        if "update-display_name" in request.POST:
            if request.POST.get("display_name"):
                profile.display_name = request.POST.get("display_name")
                profile.save()
                messages.success(request, "Display name updated successfully.")
            
            # Bio
            if request.POST.get("bio"):
                profile.bio = request.POST.get("bio")
                profile.save()
                messages.success(request, "Bio updated successfully.")

            # Fav Genre
            if request.POST.get("fav_genre"):
                genre = request.POST.get("fav_genre")
                profile.fav_genre = genre
                profile.save()
                messages.success(request, "Genre preferences updated successfully.")

        # Update Password
        if "update-password" in request.POST:
            if not request.user.check_password(request.POST.get("current_password")):
                messages.error(request, "Current password is incorrect.")
            
            elif request.POST.get("new_password") and request.POST.get("confirm_password"):
                if request.POST.get("new_password") != request.POST.get("confirm_password"):
                    messages.error(request, "New passwords do not match.")
                else:
                    request.user.set_password(request.POST.get("new_password"))
                    request.user.save()
                    messages.success(request, "Password updated successfully.")
        
        # Deactivate Account
        if "deactivate-account" in request.POST:
            if request.POST.get("deactivate_password"):
                print("Deactivate Password:", request.POST.get("deactivate_password"))
                print("User Password:", request.user.password)
                if not request.user.check_password(request.POST.get("deactivate_password")):
                    messages.error(request, "Current password is incorrect.")
                else:
                    request.user.is_active = False
                    request.user.save()
                    messages.success(request, "Account deactivated. You can reactivate it by logging back in.")
                    return redirect("sign_in")

        # Delete Account  
        if "delete-account" in request.POST:
            if request.POST.get("email_confirm") and request.POST.get("password"):
                if not request.user.check_password(request.POST.get("password")):
                    messages.error(request, "Current password is incorrect.")
                elif request.POST.get("email_confirm") != request.user.email:
                    messages.error(request, "Email confirmation does not match.")
                else:
                    request.user.delete()
                    messages.success(request, "Account deleted permanently.")
                    return redirect("sign_up")

        return redirect("settings")

    return render(request, "user/settings.html")

@login_required
def watched(request):
    watched_qs = Watched.objects.filter(user=request.user).select_related("movie")
    
    context = {
        "watched": [w.movie for w in watched_qs]
    }
    return render(request, 'user/watched.html', context)

@login_required
def watchlist(request):
    watchlist_qs = Watchlist.objects.filter(user=request.user).select_related("movie")
    
    context = {
        "watchlist": [w.movie for w in watchlist_qs]
    }
    return render(request, 'user/watchlist.html', context)