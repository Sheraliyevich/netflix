
from django.test import TestCase, Client

from movie.models import Actor, Movie
from movie.serializers import MovieSerializer


class TestGetMovieList(TestCase):
    def setUp(self) -> None:
        self.movie = Movie.objects.create(
            title="Test Movie1",
            year="2000-03-04",
            imdb="https://example.com/movie_2.mp4")

    def test_get(self):
        data = MovieSerializer(self.movie).data
        assert data['id'] is not None
        assert data['title'] == "Test Movie1"
        assert data['year'] == "2000-03-04"
        assert data['imdb'] == "https://example.com/movie_2.mp4"


# class TestOrderingMovie(TestCase):
#     def setUp(self) -> None:
#         self.movie = Movie.objects.create(
#             title="Test Movie2",
#             year="2001-03-04",
#             imdb="https://example.com/movie_2.mp4")
#
#     def test_ordering(self):
#         data = MovieSerializer(self.movie).data
#
#         assert data['id'] is not None
#         assert data['title'] == "Test Movie2"
#         assert data['year'] == "2001-03-04"
#         assert data['imdb'] == "https://example.com/movie_2.mp4"


class TestSearchMovieList(TestCase):
    def setUp(self) -> None:
        self.actor = Actor.objects.create(name="Test Actor")
        self.movie = Movie.objects.create(title="Test Movie", year="2022-03-04", imdb="https://example.com/movie_1.mp4")
        self.movie.actor.add(self.actor)
        self.client = Client()

    def test_search(self):
        response = self.client.get('/movies/?search=Test Movie')
        data = response.data

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]['title'], "Test Movie")


class TestOrderingMovie(TestCase):
    def setUp(self) -> None:
        self.actor = Actor.objects.create(name="Test Actor2")
        self.movie = Movie.objects.create(title="Test Movie2",
                                          year="2001-03-04",
                                          imdb="https://example.com/movie_2.mp4")
        self.movie.actor.add(self.actor)
        self.client = Client()

    def test_search(self):
        response = self.client.get('/movies/?ordering=[year]')
        data = response.data

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]['imdb'], "https://example.com/movie_2.mp4")
        self.assertEquals(data[0]['year'], "2001-03-04")
        self.assertEquals(data[0]['title'], "Test Movie2")
