from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class GenericMovieData(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300,blank=True)
    genre = models.CharField(max_length=50)
    release_date = models.DateTimeField(auto_now=False)
    poster_url = models.URLField(max_length=150)

    def __str__(self):
        return self.title


from django.db import models

#TMDB Movie Model Format
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    original_language = models.CharField(max_length=255)
    overview = models.TextField()
    adult = models.BooleanField(default=True)
    backdrop_path = models.URLField()
    #genre_ids = ArrayField(models.IntegerField(null=True, blank=True), blank=True) #only for postgers DB
    genre_ids = models.TextField(blank=True)
    popularity = models.IntegerField()
    poster_path = models.URLField()
    release_date = models.CharField(max_length=255)#models.DateField()
    video = models.BooleanField(default=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()




# Currently not in use
class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    phoneNumber = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=128) # Should be hashed before storing it
    image = models.ImageField(upload_to='static/user_images/')