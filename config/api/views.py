from .models import Actor, Rejissior, Genre, Movie, Comment
from .serializers import (ActorSerializer, GenreSerializer, MovieSerializer,
                          RejissiorSerializer, ActorAdminSerializer, MovieAdminSerializer, CommentSerializer)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from .permissions import MyIsAuthenticatedOrReadOnly, IsOwner

class GenreAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class GenreRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class ActorAPIView(ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ActorAdminSerializer
        return ActorSerializer

class ActorRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class RejissiorAPIView(ListCreateAPIView):
    queryset = Rejissior.objects.all()
    serializer_class = RejissiorSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        grade = self.request.query_params.get('grade')
        if grade:
            return self.queryset.filter(grade=grade)
        return self.queryset.all()
    
class RejissiorRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Rejissior.objects.all()
    serializer_class = RejissiorSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class MovieAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

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
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

class CommentAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [MyIsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        movie_id = self.kwargs.get('movie_id')
        return self.queryset.filter(movie_id=movie_id)
    
    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, id=self.kwargs.get('movie_id'))
        serializer.validated_data['user'] = self.request.user
        serializer.validated_data['movie'] = movie
        serializer.save()
        return serializer

class CommentRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [MyIsAuthenticatedOrReadOnly, IsOwner,]
    lookup_url_kwarg = 'comment_id'
