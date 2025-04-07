from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FavoriteTrackViewSet, FavoriteAlbumViewSet

router = DefaultRouter()
router.register(r'tracks', FavoriteTrackViewSet, basename='favorite-track')
router.register(r'albums', FavoriteAlbumViewSet, basename='favorite-album')

urlpatterns = [
    path('', include(router.urls)),
]
