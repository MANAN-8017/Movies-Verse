from django.shortcuts import render, redirect

# Private
def favourite(request):
    if not request.session.get('user_email'):
        return redirect('sign_in')
    return render(request, 'favourite.html')

# Private
def profile(request):
    if not request.session.get('user_email'):
        return redirect('sign_in')
    return render(request, 'profile.html')

# Private
def settings(request):
    if not request.session.get('user_email'):
        return redirect('sign_in')    
    return render(request, 'settings.html')

def sign_in(request):
    return render(request, 'sign_in.html')

def sign_up(request):
    return render(request, 'sign_up.html')

# Private
def watched(request):
    if not request.session.get('user_email'):
        return redirect('sign_in')
    return render(request, 'watched.html')

# Private
def watchlist(request):
    if not request.session.get('user_email'):
        return redirect('sign_in')
    return render(request, 'watchlist.html')