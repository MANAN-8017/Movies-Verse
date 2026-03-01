from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ProductionHouse(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=255, unique=True)

    tmdb_company_id = models.IntegerField(null=True, blank=True, unique=True)
    omdb_company_id = models.CharField(max_length=50, null=True, blank=True, unique=True)

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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(
        upload_to='userdata/profile_pic/',
        null=True,
        blank=True
    )
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    fav_genre = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
class Movie(models.Model):
    tmdb_id      = models.IntegerField(unique=True)
    omdb_id      = models.CharField(max_length=20, unique=True)
    title        = models.CharField(max_length=300)
    poster       = models.URLField(max_length=500, blank=True)
    release_year = models.CharField(max_length=10, blank=True)
    runtime      = models.IntegerField(default=0, help_text="Runtime in minutes")
    genres       = models.CharField(max_length=200, blank=True, help_text="Comma-separated genre names")
    overview     = models.TextField(blank=True)
    director     = models.CharField(max_length=200, blank=True)
    origin_country = models.CharField(max_length=10, blank=True, help_text="ISO 3166-1 country code, e.g. 'US'")

    def __str__(self):
        return self.title
    
class Watchlist(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie    = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')   # no duplicates
        ordering = ['-added_on']

    def __str__(self):
        return f"{self.user.username} → watchlist → {self.movie.title}"

class Watched(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watched_movies')
    movie      = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_on = models.DateTimeField(default=timezone.now)
    progress   = models.IntegerField(default=100, help_text="0-100. < 100 means still watching.")

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-watched_on']

    def __str__(self):
        return f"{self.user.username} watched {self.movie.title}"

    @property
    def is_completed(self):
        return self.progress == 100

class Favourite(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    movie    = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_on']

    def __str__(self):
        return f"{self.user.username} ❤ {self.movie.title}"

class Rating(models.Model):
    STAR_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie    = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    rating   = models.IntegerField(choices=STAR_CHOICES)
    rated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-rated_on']

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title} {self.rating}/5"

class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    movie      = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    text       = models.TextField(max_length=2000)
    rating     = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    likes      = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} reviewed {self.movie.title}"

class Like(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    movie    = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    liked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-liked_on']

    def __str__(self):
        return f"{self.user.username} 👍 {self.movie.title}"

class SearchHistory(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    query       = models.CharField(max_length=300)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']

    def __str__(self):
        return f"{self.user.username} searched '{self.query}'"