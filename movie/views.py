from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from movie.models import Movie, Actor, Comment
from movie.serializers import MovieSerializer, ActorSerializer, CommentSerializer


class MovieActorAPIView(APIView):
    def get(self, request, id):
        movie = Movie.objects.get(id=id)
        actors = movie.actor.all()
        serializer = ActorSerializer(actors, many=True)

        return Response(data=serializer.data)


class CommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(user_id=request.user)
        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        comment = Comment.objects.get(id=pk)
        comment.delete()
        print(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user
        serializer.save()


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['genre']
    ordering_fields = ['imdb']

    @action(detail=True, methods=['POST'])
    def add_actor(self, request, *args, **kwargs):
        movie = self.get_object()
        actor = Actor.objects.get_or_create(name=request.data['name'],
                                            birthdate=request.data['birthdate'],
                                            gender=request.data['gender'])[0]
        serializer = ActorSerializer(actor)
        movie.actor.add(actor)
        movie.save()

        return Response(data=serializer.data)

    @action(detail=True, methods=['POST'], url_path='remove-actor')
    def RemoveActor(self, request, *args, **kwargs):
        movie = self.get_object()
        actor = movie.actor.last()
        movie.actor.remove(actor)
        movie.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
        

class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
