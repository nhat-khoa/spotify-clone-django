from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserFollowedArtistViewSet, UserFollowedPodcastViewSet, UserFollowedPlaylistViewSet,
    UserSavedTrackViewSet, UserSavedAlbumViewSet, UserSavedEpisodeViewSet
)

router = DefaultRouter()
router.register(r'user-followed-artists', UserFollowedArtistViewSet, basename='user-followed-artist')
router.register(r'user-followed-podcasts', UserFollowedPodcastViewSet, basename='user-followed-podcast')
router.register(r'user-followed-playlists', UserFollowedPlaylistViewSet, basename='user-followed-playlist')
router.register(r'user-saved-tracks', UserSavedTrackViewSet, basename='user-saved-track')
router.register(r'user-saved-albums', UserSavedAlbumViewSet, basename='user-saved-album')
router.register(r'user-saved-episodes', UserSavedEpisodeViewSet, basename='user-saved-episode')

urlpatterns = [
    path('', include(router.urls)),
]
