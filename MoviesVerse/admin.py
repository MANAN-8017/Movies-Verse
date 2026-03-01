from .models import *
from django.contrib import admin

admin.site.register(ProductionHouse)
admin.site.register(Movie)
admin.site.register(Profile)
admin.site.register(Watchlist)
admin.site.register(Watched)
admin.site.register(Favourite)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(SearchHistory)

admin.site.site_header = "MoviesVerse Admin"
admin.site.index_title = "Admin Dashboard"
admin.site.site_title = "MoviesVerse Admin Portal"