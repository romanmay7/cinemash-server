from django.contrib import admin
from .models import GenericMovieData
from .models import Movie

# Register your models here.

class CinemashAdmin(admin.ModelAdmin):
    list_display = ('id', 'tmdb_id', 'title', 'original_title', 'original_language', 'overview','adult',
                    'backdrop_path','genre_ids','popularity','poster_path','release_date','video','vote_average','vote_count')
    #list_display = ('id', 'title', 'description', 'genre', 'release_date', 'poster_url')
    #list_display_links = ('id', 'title')
    #search_fields = ('id', 'title', 'description', 'genre', 'release_date')
    #list_editable = ('genre','release_date')
    #list_filter = ('genre','release_date')


#admin.site.register(GenericMovieData, CinemashAdmin, )
admin.site.register(Movie, CinemashAdmin, )

