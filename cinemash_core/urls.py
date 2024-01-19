from django.urls import path
from rest_framework import routers
from .views import UserViewSet, GenericMovieDataViewSet

#router = routers.DefaultRouter()
#router.register('api/movies', GenericMovieViewSet, 'movies')

#urlpatterns = router.urls

urlpatterns = [

    path('movies/', GenericMovieDataViewSet.as_view({'post': 'create', 'get': 'list'}), name="movies"),
    path('users/', UserViewSet.as_view({'post': 'create', 'get': 'list'})),  # Add 'get' for list view,

]











