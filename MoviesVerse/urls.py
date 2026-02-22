# MoviesVerse/urls.py

from django.urls import path
from django.conf.urls.static import static

from mySite import settings
from . import views

urlpatterns = [
    # Default
    path('', views.index, name='index'),
    
    # Auth
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),

    # Private
    path('favourite/', views.favourite, name='favourite'),
    path('profile/', views.profile, name='profile'),
    path('watched/', views.watched, name='watched'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('settings/', views.settings, name='settings'),

    # Public
    path('index/', views.index, name='index'),
    path('oppenheimer/', views.oppenheimer, name='oppenheimer'),
    path('upcoming/', views.upcoming, name='upcoming'),
    path('popular/', views.popular, name='popular'),
    path('trending/', views.trending, name='trending'),

    # Legal
    path('help/', views.help, name='help'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),

    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)