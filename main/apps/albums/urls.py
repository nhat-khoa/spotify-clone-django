from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, AlbumArtistViewSet

router = DefaultRouter()
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'album-artists', AlbumArtistViewSet, basename='album-artist')

urlpatterns = [
    path('', include(router.urls)),
]