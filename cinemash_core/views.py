from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from cinemash_core.serializers import GenericMovieDataSerializer

from rest_framework import viewsets, status

from .models import GenericMovieData
from .serializers import UserSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Override create method to automatically set password
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        user.set_password(user.password)  # Set password securely
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def list(self, request):
        queryset = self.get_queryset()  # Retrieve all users
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class GenericMovieDataViewSet(viewsets.ModelViewSet):
    queryset = GenericMovieData.objects.all()
    serializer_class = GenericMovieDataSerializer
    http_method_names = ['post', 'get']  # Explicitly allow POST

