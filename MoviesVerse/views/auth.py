from ..models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
import re


def validate_name(name):
    pattern = r'^[A-Za-z ]+$'
    return bool(re.fullmatch(pattern, name))


def sign_up(request):
    if request.method == 'POST':

        first_name = request.POST.get("first_name", "").strip().lower()
        last_name = request.POST.get("last_name", "").strip().lower()
        display_name = request.POST.get("display_name", "").strip()
        username = request.POST.get("username", "").strip().lower()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Name Validation
        if not first_name or not last_name:
            return render(request, "sign_up.html", {
                "error": "First name and last name cannot be empty."
            })

        if not validate_name(first_name):
            return render(request, "sign_up.html", {
                "error": "First name must contain only alphabets."
            })

        if not validate_name(last_name):
            return render(request, "sign_up.html", {
                "error": "Last name must contain only alphabets."
            })

        # Display Name
        if display_name and len(display_name) < 3:
            return render(request, "sign_up.html", {
                "error": "Display name must be at least 3 characters long."
            })

        # Username
        if not username:
            return render(request, "sign_up.html", {
                "error": "Username cannot be empty."
            })

        if len(username) < 3:
            return render(request, "sign_up.html", {
                "error": "Username must be at least 3 characters long."
            })

        if User.objects.filter(username__iexact=username).exists():
            return render(request, "sign_up.html", {
                "error": "Username already exists."
            })

        # Email
        if not email:
            return render(request, "sign_up.html", {
                "error": "Email cannot be empty."
            })

        if User.objects.filter(email__iexact=email).exists():
            return render(request, "sign_up.html", {
                "error": "Email already exists."
            })

        # Password
        if not password or not confirm_password:
            return render(request, "sign_up.html", {
                "error": "Password fields cannot be empty."
            })

        if password != confirm_password:
            return render(request, "sign_up.html", {
                "error": "Passwords do not match."
            })

        # Create User
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email.strip().lower(),
            password=password
        )

        Profile.objects.create(user=user, display_name=display_name)

        return redirect("sign_in")

    return render(request, "sign_up.html")

def sign_in(request):
    next_url = request.GET.get('next')

    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')
        next_url_post = request.POST.get('next')

        try:
            user_obj = User.objects.get(email__iexact=email)
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
            
            if user is None and user_obj.check_password(password):
                user_obj.is_active = True
                user_obj.save()
                user = user_obj
                
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)

            if next_url_post and url_has_allowed_host_and_scheme(next_url_post, allowed_hosts={request.get_host()}):
                return redirect(next_url_post)

            return redirect('index')

        return render(request, 'sign_in.html', { 'error': 'Invalid email or password', 'next': next_url})

    return render(request, 'sign_in.html', {'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('sign_in')