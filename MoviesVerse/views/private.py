import os
from urllib import request
from ..models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()
@login_required
def favourite(request):
    return render(request, 'favourite.html')

@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def settings(request):

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

    return render(request, "settings.html")

@login_required
def watched(request):
    return render(request, 'watched.html')

@login_required
def watchlist(request):
    return render(request, 'watchlist.html')