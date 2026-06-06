from django.urls import path
from .views import (MovieAPIView, ActorAPIView, GenreAPIView, RejissiorAPIView,
                    ActorRetrieveAPIView, RejissiorRetrieveAPIView, GenreRetrieveAPIView, MovieRetrieveAPIView, CommentAPIView, CommentRetrieveAPIView)

urlpatterns = [
    path('movies/', MovieAPIView.as_view()),
    path('movies/<int:pk>/', MovieRetrieveAPIView.as_view()),
    path('movies/genres/<int:pk>/', MovieAPIView.as_view()),
    path('actors/', ActorAPIView.as_view()),
    path('actors/<int:pk>/', ActorRetrieveAPIView.as_view()),
    path('actors/grade/<int:pk>/', ActorAPIView.as_view()),
    path('genres/', GenreAPIView.as_view()),
    path('genres/<int:pk>/', GenreRetrieveAPIView.as_view()),
    path('rejissiors/', RejissiorAPIView.as_view()),
    path('rejissiors/<int:pk>/', RejissiorRetrieveAPIView.as_view()),
    path('movies/<int:movie_id>/comments/', CommentAPIView.as_view()),
    path('movies/<int:movie_id>/comments/<int:comment_id>/', CommentRetrieveAPIView.as_view()),
    
]