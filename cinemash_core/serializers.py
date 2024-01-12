from rest_framework import serializers
from .models import GenericMovieData

class GenericMovieDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericMovieData
        fields = '__all__'