from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from MoviesVerse.models import ProductionHouse

def production_house_dashboard(request):
    ph_id = request.session.get('production_house_id')
    if not ph_id:
        return redirect('sign_in')
    
    production_house = ProductionHouse.objects.get(id=ph_id)
    return render(request, 'production_house/production_house_dashboard.html', {
        'production': production_house,  # ← was 'production_house', must be 'production'
        'movies': [],
    })

def production_analytics(request):
    ph_id = request.session.get('production_house_id')
    if not ph_id:
        return redirect('sign_in')
    
    production_house = ProductionHouse.objects.get(id=ph_id)
    return render(request, 'production_house/production_analytics.html', {
        'production': production_house,
        'movies': [],
    })


def add_promotion(request):
    ph_id = request.session.get('production_house_id')
    if not ph_id:
        return redirect('sign_in')
    
    production_house = ProductionHouse.objects.get(id=ph_id)

    if request.method == 'POST':
        # handle form submission later
        pass

    return render(request, 'production_house/add_promotion.html', {
        'production': production_house,
        'movies': [],
        'promotions': [],
    })