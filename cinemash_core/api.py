from .models import GenericMovieData
from rest_framework import viewsets,permissions
from .serializers import GenericMovieDataSerializer

class GenericMovieViewSet(viewsets.ModelViewSet):
    queryset = GenericMovieData.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = GenericMovieDataSerializer