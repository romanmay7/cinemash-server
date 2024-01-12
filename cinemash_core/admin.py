from django.contrib import admin
from .models import GenericMovieData

# Register your models here.

class CinemashAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'genre', 'release_date', 'poster_url')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'description', 'genre', 'release_date')
    list_editable = ('genre','release_date')
    list_filter = ('genre','release_date')


admin.site.register(GenericMovieData, CinemashAdmin)


