from django.db import models

class UserProfile(models.Model):
    # User
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='userdata/profile_pic/Profile_Pic.jpeg', null=True, blank=True)
    def __str__(self):
        return self.username