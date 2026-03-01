from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.http import url_has_allowed_host_and_scheme

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'sign_up.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'sign_up.html', {
                'error': 'Email already exists'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(user=user)

        return redirect('sign_in')

    return render(request, 'sign_up.html')


def sign_in(request):
    next_url = request.GET.get('next')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url_post = request.POST.get('next')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)

            if next_url_post and url_has_allowed_host_and_scheme(
                next_url_post,
                allowed_hosts={request.get_host()}
            ):
                return redirect(next_url_post)

            return redirect('index')

        return render(request, 'sign_in.html', {
            'error': 'Invalid email or password',
            'next': next_url
        })

    return render(request, 'sign_in.html', {
        'next': next_url
    })


def logout_view(request):
    logout(request)
    return redirect('sign_in')