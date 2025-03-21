from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FolderViewSet, PlaylistViewSet, PlaylistTrackPodcastViewSet

router = DefaultRouter()
router.register(r'folders', FolderViewSet, basename='folder')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'playlist-items', PlaylistTrackPodcastViewSet, basename='playlist-item')

urlpatterns = [
    path('', include(router.urls)),
]
