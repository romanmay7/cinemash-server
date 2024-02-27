from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from cinemash_core.serializers import GenericMovieDataSerializer

from rest_framework import viewsets, status

from .models import GenericMovieData
from .serializers import UserSerializer

import json
import requests

from .models import Movie
from django.http import JsonResponse


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

def get_and_store_movies(request):
    api_key = "YOUR_TMDB_API_KEY"  # Replace with your key
    api_key = ""
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data["results"]  # Assuming "results" key holds movie data

        # Convert and save movies
        for movie_data in movies:
            movie = Movie(
                tmdb_id=movie_data["id"],
                title=movie_data["title"],
                original_title=movie_data.get("original_title"),
                original_language=movie_data.get("original_language"),
                overview=movie_data["overview"],
                adult=movie_data.get("adult", True),  # Handle potential missing data with default
                backdrop_path=f"https://image.tmdb.org/t/p/w500{movie_data.get('backdrop_path')}",
                # genre_ids=movie_data.get("genre_ids", []),  # Handle potential missing data with empty list
                genre_ids=json.dumps(movie_data.get("genre_ids", [])),
                popularity=movie_data.get("popularity"),
                poster_path=f"https://image.tmdb.org/t/p/w185{movie_data.get('poster_path')}",
                release_date=movie_data.get("release_date"),
                video=movie_data.get("video", True),  # Handle potential missing data with default
                vote_average=movie_data.get("vote_average"),
                vote_count=movie_data.get("vote_count"),
            )

            #print(f'{"genre_ids"} : {type(movie.genre_ids)}')

            movie.save()

        return HttpResponse("Movies from TMDB saved successfully!")
    else:
        return HttpResponse(f"Error: {response.status_code}", status=response.status_code)




def get_movies_json_from_db(request):
    movies = Movie.objects.all()  # Retrieve all movies from DB

    # Convert movies to JSON format
    data = []
    for movie in movies:
        data.append({
            "id": movie.id,
            "tmdb_id": movie.tmdb_id,
            "title": movie.title,
            "original_title": movie.original_title,
            "original_language": movie.original_language,
            "overview": movie.overview,
            "adult": movie.adult,
            "backdrop_path": movie.backdrop_path,
            "genre_ids": json.loads(movie.genre_ids) if movie.genre_ids else [],  # Handle potential null values
            "popularity":movie.popularity,
            "poster_path": movie.poster_path,
            "release_date":movie.release_date,
            "video": movie.video,
            "vote_average": movie.vote_average,
            "vote_count": movie.vote_count
        })

    return JsonResponse(data, safe=False)  # Ensure proper JSON serialization
