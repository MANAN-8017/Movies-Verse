from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from ..models import UserProfile

def sign_up_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            return render(request, 'sign_up.html', {'error': 'Passwords do not match'})

        if UserProfile.objects.filter(email=email).exists():
            return render(request, 'sign_up.html', {'error': 'Email already exists'})

        UserProfile.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        messages.success(request, 'Account created. Please sign in.')
        return redirect('sign_in')

    return render(request, 'sign_up.html')

def sign_in_form(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = UserProfile.objects.filter(email=email).first()

        if user and check_password(password, user.password):
            request.session['user_email'] = user.email
            return redirect('index')

        return render(request, 'sign_in.html', {'error': 'Invalid credentials'})

    return render(request, 'sign_in.html')

def logout(request):
    request.session.flush()
    return redirect('sign_in')