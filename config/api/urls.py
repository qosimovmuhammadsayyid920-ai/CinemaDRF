from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import MovieAPIViewSet, ActorAPIViewSet, GenreAPIViewSet, RejissiorAPIViewSet, CommentAPIViewSet

router = DefaultRouter()
router.register('movies', MovieAPIViewSet)
router.register('actors', ActorAPIViewSet)
router.register('genres', GenreAPIViewSet)
router.register('rejissiors', RejissiorAPIViewSet)

urlpatterns = [
    path('movies/<int:movie_id>/comments/',
         CommentAPIViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='comment-list'),

    path('movies/<int:movie_id>/comments/<int:comment_id>/',
         CommentAPIViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='comment-detail'),
        
    path('', include(router.urls))
]