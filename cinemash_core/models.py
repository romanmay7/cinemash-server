from django.db import models

# Create your models here.

class GenericMovieData(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300,blank=True)
    genre = models.CharField(max_length=50)
    release_date = models.DateTimeField(auto_now=False)
    poster_url = models.URLField(max_length=150)

    def __str__(self):
        return self.title



# Currently not in use
class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    phoneNumber = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=128) # Should be hashed before storing it
    image = models.ImageField(upload_to='static/user_images/')