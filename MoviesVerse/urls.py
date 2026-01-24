# MoviesVerse/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Default
    path('', views.index, name='index'),
    
    # Auth
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout, name='logout'),

    # Private
    path('index/', views.index, name='index'),
    path('favourite/', views.favourite, name='favourite'),
    path('profile/', views.profile, name='profile'),
    path('watched/', views.watched, name='watched'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('settings/', views.settings, name='settings'),

    # Public
    path('coming_soon/', views.coming_soon, name='coming_soon'),
    path('oppenheimer/', views.oppenheimer, name='oppenheimer'),
    path('popular/', views.popular, name='popular'),
    path('trending/', views.trending, name='trending'),

    # Legal
    path('help/', views.help, name='help'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),


    path('sign_up/submit/', views.sign_up_form, name='sign_up_form'),  # route for sign up form
    path('sign_in/submit/', views.sign_in_form, name='sign_in_form'),  # route for login form
]