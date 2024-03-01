from rest_framework import serializers
from .models import GenericMovieData, UserProfileInfo
from django.contrib.auth.models import User

class GenericMovieDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericMovieData
        fields = '__all__'



# create a serializer for user registration
class UserProfileSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True)

        class Meta:
            model = UserProfileInfo
            fields = ('username', 'password', 'full_name', 'location',
                      'favorite_genres_ids', 'age', 'bio', 'phone_number', 'email', 'joined_date', 'last_login')
            extra_kwargs = {'password': {'required': True}}

        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password']
            )
            user_profile = UserProfileInfo.objects.create(user=user, **validated_data)
            return user_profile


#create user
def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user