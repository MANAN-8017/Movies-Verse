from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='sign_in')
def favourite(request):
    return render(request, 'favourite.html')

@login_required(login_url='sign_in')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='sign_in')
def settings(request):
    return render(request, 'settings.html')

@login_required(login_url='sign_in')
def watched(request):
    return render(request, 'watched.html')

@login_required(login_url='sign_in')
def watchlist(request):
    return render(request, 'watchlist.html')