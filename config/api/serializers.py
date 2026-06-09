from rest_framework import serializers
from .models import Actor, Rejissior, Genre, Movie, Comment
from django.contrib.auth.models import User

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'birth_year']
        read_only_fields = ['id']

class ActorAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['name', 'birth_year', 'avatar']
        read_only_fields = ['id']

class RejissiorSerializer(serializers.ModelSerializer):
    # movies = serializers.StringRelatedField(many=True)
    # movies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # movies = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')
    # movies = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    url = serializers.HyperlinkedIdentityField(view_name='rejissior-detail')
    
    class Meta:
        model = Rejissior
        fields = ['name', 'birth_year', 'grade', 'movies', 'url']
        read_only_fields = ['id']

class MovieSerializerForGenre(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_year', 'poster', 'rejissior', 'actor']

class GenreSerializer(serializers.ModelSerializer): 
    # movies = serializers.StringRelatedField(many=True)
    # movies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # movies = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')
    # movies = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    # url = serializers.HyperlinkedIdentityField(view_name='movie-detail')

    movies = MovieSerializerForGenre(many=True)

    class Meta:
        model = Genre
        fields = "__all__"
        read_only_fields = ['id']
    
    def create(self, validated_data):
        movies = validated_data.pop('movies')
        genre = Genre.objects.create(**validated_data)
        for movie in movies:
            Movie.objects.create(genre=genre, **movie)
        return genre
    
    def update(self, instance, validated_data):
        movies = validated_data.pop('movies')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.movies.all().delete()
        for movie in movies:
            Movie.objects.create(genre=instance, **movie)
        return instance

class MovieSerializer(serializers.ModelSerializer):
    genre_write = serializers.ChoiceField(
        choices=Genre.objects.all(),
        write_only=True
    )
    rejissior_write = serializers.ChoiceField(
        choices=Rejissior.objects.all(),
        write_only = True
    )
    actor_write = serializers.ChoiceField(
        choices=Actor.objects.all(),
        write_only = True
    )

    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_year', 'genre', 'rejissior', 'actor', 'genre_write', 'rejissior_write', 'actor_write']
        read_only_fields = ['id', 'rejissior_write', 'genre_write', 'actor_write', ]
        depth = 1

    def create(self, validated_data):
        genre_write = validated_data.pop('genre_write')
        rejissior_write = validated_data.pop('rejissior_write')
        actor_write = validated_data.pop('actor_write')
        movie = Movie.objects.create(
            genre=genre_write,
            actor=actor_write,
            rejissior=rejissior_write,
            **validated_data
        )
        movie.save()
        return movie
    
    def update(self, instance, validated_data):
        instance.genre = validated_data.pop('genre_write', instance.genre)
        instance.actor = validated_data.pop('actor_write', instance.actor)
        instance.rejissior = validated_data.pop('rejissior_write', instance.rejissior)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class MovieAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_year', 'poster', 'genre', 'rejissior', 'actor',]
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',]

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'user', 'movie' ]
        read_only_fields = ['id', 'user', 'movie']
        depth = 1
