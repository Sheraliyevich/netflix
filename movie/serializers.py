from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movie.models import Movie, Actor, Comment


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'birthdate', 'gender')

    def validate_birthdate(self, value):
        if value.year < 1950:
            raise ValidationError(detail='birthdate must be greater than 01.01.1950')

        return value


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user_id', 'movie_id', 'text', 'created_date')


class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer
    comments = CommentSerializer

    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'imdb', 'genre', 'actor')
