from math import sqrt

from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from cinemash_core.serializers import GenericMovieDataSerializer

from rest_framework import viewsets, status

from .models import GenericMovieData
from .serializers import UserProfileSerializer

import json
import requests

from .models import Movie, UserProfileInfo
from django.http import JsonResponse
from fuzzywuzzy import fuzz  # Import fuzzywuzzy library for string similarity


# Create your views here.

#class UserViewSet(viewsets.ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

    # Override create method to automatically set password
  #  def create(self, request):
  #      serializer = self.serializer_class(data=request.data)
  #       serializer.is_valid(raise_exception=True)
  #      user = self.perform_create(serializer)
  #      user.set_password(user.password)  # Set password securely
  #      user.save()
 #       return Response(serializer.data, status=status.HTTP_201_CREATED)
    #def list(self, request):
  #      queryset = self.get_queryset()  # Retrieve all users
  #      serializer = UserSerializer(queryset, many=True)
  #      return Response(serializer.data)


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

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        print(json.loads(request.body.decode('utf-8')))
        serializer = UserProfileSerializer(data=json.loads(request.body.decode('utf-8')))
        if serializer.is_valid():
            serializer.save()

            # Generate auth token (optional, adjust as needed)
            #token, _ = Token.objects.create(user=user)

            return HttpResponse(status=201)

        else:
            print(serializer.errors)
            return HttpResponse(status=400)  # Bad request status code with error messages
    else:
        return HttpResponse(status=405)  # Method not allowed status code

class UserProfileList(APIView):
        def get(self, request):
            user_profiles = UserProfileInfo.objects.all()
            serializer = UserProfileSerializer(user_profiles, many=True)
            return Response(serializer.data)

@csrf_exempt
def find_10_most_similar_users(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    print(username)
    try:
        user_profile = UserProfileInfo.objects.filter(username=username).get()
        print(user_profile)
        return find_N_most_similar_users(user_profile, 10)
    except UserProfileInfo.DoesNotExist:
        return Response(None)  # Handle the case where no profile exists


def find_N_most_similar_users(user_profile, N, similarity_threshold=0.6):
    """
    Finds the N most similar users to the given user profile based on their favorite genres
    And based on other user profile attributes.

    Args:
        user_profile (UserProfileInfo): The user profile object for whom to find similar users.
        N (int): The number of most similar users to find.
        similarity_threshold (float, optional): The minimum similarity score
            required to be considered similar. Defaults to 0.6.

    Returns:
        JSON: containing the user objects
    """

    if not user_profile or not user_profile.favorite_genres_ids:
        return []  # Handle case where genres are missing

    user_genres = set(convert_favorite_genres_to_array(user_profile.favorite_genres_ids))

    # Build a queryset of all users excluding the given user's associated user
    similar_users = UserProfileInfo.objects.exclude(username=user_profile.username)
    #print(similar_users)

    # Efficiently calculate cosine similarity for each user
    genre_weight = 0.5
    location_weight = 0.2
    age_weight = 0.2
    bio_weight = 0.1

    user_similarities = []
    for potential_user in similar_users:
        potential_user_genres = set(convert_favorite_genres_to_array(potential_user.favorite_genres_ids))
        print(potential_user_genres)
        intersection = user_genres.intersection(potential_user_genres)
        union = user_genres.union(potential_user_genres)

        genre_similarity = len(intersection) / sqrt(len(user_genres) * len(potential_user_genres)) if union else 0

        location_similarity = fuzz.ratio(user_profile.location, potential_user.location) / 100

        age_similarity = 1 - abs(user_profile.age - potential_user.age) / 100  # Adjust scaling as needed

        # Consider using a similarity function for bio comparison (e.g., Levenshtein distance)
        bio_similarity = 0.5  # Placeholder, replace with appropriate bio similarity calculation

        # Combine weighted similarities
        similarity = (genre_weight * genre_similarity +
                      location_weight * location_similarity +
                      age_weight * age_similarity +
                      bio_weight * bio_similarity)

        print("Similarity Score:" + str(similarity))


        user_similarities.append((potential_user, similarity))

    # Filter and sort by similarity in descending order
    filtered_similarities = [
        (user, score) for user, score in user_similarities if score >= similarity_threshold
    ]

    # Extract user_profile objects
    user_profile_objects = [
        user_info[0] for user_info in filtered_similarities[:N]
    ]

    #print(user_profile_objects)

    serializer = UserProfileSerializer(user_profile_objects, many=True)
    #print(type(serializer.data))

    return JsonResponse(serializer.data,safe=False) #user_profile_objects



def convert_favorite_genres_to_array(favorite_genres_ids):
  """
  Converts the given favorite_genres_ids to a list of integers.

  Args:
      favorite_genres_ids: The value to be converted.

  Returns:
      A list of integers containing the genre IDs.
  """

  if isinstance(favorite_genres_ids, str):
    # Try removing square brackets if present
    try:
      without_brackets = favorite_genres_ids.strip('[]')
      listOfInts = list(map(int, without_brackets.split(',')))
      print(listOfInts)
      return listOfInts
    except ValueError:
      # If removing brackets fails, handle the original string
      return list(map(int, favorite_genres_ids.split(',')))
  elif isinstance(favorite_genres_ids, (list, set)):
    # If it's already a list or set, convert to list of integers
    return list(favorite_genres_ids)
  else:
    # Handle unexpected data types (optional)
    raise ValueError("Unsupported data type for favorite_genres_ids")
