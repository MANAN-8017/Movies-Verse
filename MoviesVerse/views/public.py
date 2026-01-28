from django.shortcuts import render

# Public
def index(request):
    # email = request.session.get('user_email')
    return render(request, 'index.html')

# Public
def oppenheimer(request):
    # email = request.session.get('user_email')
    return render(request, 'oppenheimer.html')

# Public
def popular(request):
    # email = request.session.get('user_email')
    return render(request, 'popular.html')

# Public
def trending(request):
    # email = request.session.get('user_email')
    return render(request, 'trending.html')

# Public
def upcoming(request):
    # email = request.session.get('user_email')
    return render(request, 'upcoming.html')

# Public
def help(request):
    # email = request.session.get('user_email')
    return render(request, 'help.html')

# Public
def privacy_policy(request):
    # email = request.session.get('user_email')
    return render(request, 'privacy_policy.html')

# Public
def terms_of_use(request):
    # email = request.session.get('user_email')
    return render(request, 'terms_of_use.html')