from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Actor(models.Model):
    MALE = "Male"
    FEMALE = "Female"
    GENDERS = (
        (MALE, "Male"),
        (FEMALE, "Female")
    )

    name = models.CharField(max_length=150, blank=False, null=False)
    birthdate = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=GENDERS)

    def __str__(self):
        return self.name


class Movie(models.Model):

    ACTION = "Action"
    DRAMA = "Drama"
    COMEDY = "Comedy"
    GENRES = (
        (ACTION, "Action"),
        (DRAMA, "Drama"),
        (COMEDY, "Comedy")
    )

    title = models.CharField(max_length=150, blank=False, null=False)
    year = models.DateField()
    imdb = models.URLField()
    genre = models.CharField(max_length=50, choices=GENRES, blank=True, null=True)
    actor = models.ManyToManyField(Actor, related_name="movie_actor")

    def __str__(self):
        return self.title


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comment_movie")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    text = models.CharField(max_length=1024)
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.text
