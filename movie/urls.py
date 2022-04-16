from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from movie.views import ActorViewSet, MovieViewSet, MovieActorAPIView, CommentAPIView

router = DefaultRouter()
router.register('actors', ActorViewSet),
router.register('movies', MovieViewSet),

error = 42/0

urlpatterns = [
   path('', include(router.urls)),
   path('movies/<int:id>/actors/', MovieActorAPIView.as_view(), name="movie-actors"),
   path('comment/', CommentAPIView.as_view(), name="comment"),
   path('comment/<int:pk>/', CommentAPIView.as_view(), name="comment"),
   path('auth/', obtain_auth_token)
]
