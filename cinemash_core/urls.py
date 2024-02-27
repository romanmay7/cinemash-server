from django.urls import path
from rest_framework import routers
from .views import UserViewSet, GenericMovieDataViewSet, get_and_store_movies, get_movies_json_from_db,Movie

#router = routers.DefaultRouter()
#router.register('api/movies', GenericMovieViewSet, 'movies')

#urlpatterns = router.urls

urlpatterns = [

    #path('movies/', GenericMovieDataViewSet.as_view({'post': 'create', 'get': 'list'}), name="movies"),
    path('users/', UserViewSet.as_view({'post': 'create', 'get': 'list'})),  # Add 'get' for list view,
    path("get_movies/", get_and_store_movies, name="get_movies"),
    path("get_movies_json_from_db/", get_movies_json_from_db, name="get_movies_json_from_db"),

]











