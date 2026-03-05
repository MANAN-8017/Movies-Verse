from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def oppenheimer(request):
    return render(request, 'oppenheimer.html')

def popular(request):
    return render(request, 'popular.html')

def trending(request):
    return render(request, 'trending.html')

def upcoming(request):
    return render(request, 'upcoming.html')

def help(request):
    return render(request, 'help.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')