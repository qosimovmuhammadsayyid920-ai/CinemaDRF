from rest_framework import serializers
from .models import Actor, Rejissior, Genre, Movie

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
    class Meta:
        model = Rejissior
        fields = ['name', 'birth_year', 'grade']
        read_only_fields = ['id']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
        read_only_fields = ['id']

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