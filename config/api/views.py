from .models import Actor, Rejissior, Genre, Movie
from .serializers import (ActorSerializer, GenreSerializer, MovieSerializer,
                          RejissiorSerializer, ActorAdminSerializer, MovieAdminSerializer)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class GenreAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class GenreRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class ActorAPIView(ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ActorAdminSerializer
        return ActorSerializer

class ActorRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class RejissiorAPIView(ListCreateAPIView):
    queryset = Rejissior.objects.all()
    serializer_class = RejissiorSerializer

    def get_queryset(self):
        grade = self.request.query_params.get('grade')
        if grade:
            return self.queryset.filter(grade=grade)
        return self.queryset.all()
    
class RejissiorRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Rejissior.objects.all()
    serializer_class = RejissiorSerializer
    
class MovieAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        genre = self.request.query_params.get('genre')
        if genre:
            return self.queryset.filter(genre=genre)
        return self.queryset.all()
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return MovieAdminSerializer
        return MovieSerializer
    
class MovieRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer