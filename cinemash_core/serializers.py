from rest_framework import serializers
from .models import GenericMovieData
from django.contrib.auth.models import User

class GenericMovieDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericMovieData
        fields = '__all__'



# create a serializer for user registration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}  # Hide password in responses

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user