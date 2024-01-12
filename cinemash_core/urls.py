from rest_framework import routers
from .api import GenericMovieViewSet

router = routers.DefaultRouter()
router.register('api/movies', GenericMovieViewSet, 'movies')

urlpatterns = router.urls