from django.contrib import admin
from .models import ProductionHouse, UserProfile

admin.site.register(UserProfile)
admin.site.register(ProductionHouse)