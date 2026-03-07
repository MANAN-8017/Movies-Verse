from . import views
from mySite import settings
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    # Default
    path('', views.index, name='index'),
    
    # Auth
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),

    # Private
    path('profile/', views.profile, name='profile'),
    path('watched/', views.watched, name='watched'),
    path('favourite/', views.favourite, name='favourite'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('settings/', views.settings_page, name='settings'),

    # Public
    path('index/', views.index, name='index'),
    path('popular/', views.popular, name='popular'),
    path('trending/', views.trending, name='trending'),
    path('upcoming/', views.upcoming, name='upcoming'),

    # Legal
    path('help/', views.help, name='help'),
    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

    path("search/", views.search_movies, name="search_movies"),
    path("movie/<str:imdb_id>/", views.movie_detail, name="movie_detail"),
    
     #production house
    path('add_promotion/', views.add_promotion, name='add_promotion'),
    path('production_analytics/', views.production_analytics, name='production_analytics'),
    path('production_house_dashboard/', views.production_house_dashboard, name='production_house_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)