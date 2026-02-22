from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    profile_pic = models.ImageField(
        upload_to='userdata/profile_pic/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class ProductionHouse(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=255, unique=True)

    tmdb_company_id = models.IntegerField(null=True, blank=True, unique=True)
    imdb_company_id = models.CharField(max_length=50, null=True, blank=True, unique=True)

    logo = models.ImageField(
        upload_to='userdata/production_house_logo/',
        null=True,
        blank=True
    )

    founded_year = models.IntegerField(null=True, blank=True)
    headquarters = models.CharField(max_length=255, blank=True)

    contact_number = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name