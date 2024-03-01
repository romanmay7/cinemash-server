from django.urls import path
#from rest_framework import routers
#from .views import UserViewSet, GenericMovieDataViewSet
from .views import get_and_store_movies, get_movies_json_from_db, signup, UserProfileList, find_10_most_similar_users

#router = routers.DefaultRouter()
#router.register('api/movies', GenericMovieViewSet, 'movies')

#urlpatterns = router.urls

urlpatterns = [

    #path('movies/', GenericMovieDataViewSet.as_view({'post': 'create', 'get': 'list'}), name="movies"),
   # path('users/', UserViewSet.as_view({'post': 'create', 'get': 'list'})),  # Add 'get' for list view,
    path("get_movies/", get_and_store_movies, name="get_movies"),
    path("get_movies_json_from_db/", get_movies_json_from_db, name="get_movies_json_from_db"),
    path("signup/", signup, name="signup"),
    path('userprofiles/', UserProfileList.as_view()),
    path("find_10_most_similar_users/", find_10_most_similar_users, name="find_10_most_similar_users")


]











