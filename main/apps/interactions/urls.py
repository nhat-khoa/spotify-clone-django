from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LibraryViewSet
from .playlist_views import PlaylistViewSet
from .artist_views import ArtistViewSet
from .podcast_views import PodcastViewSet  
from .episode_views import PodcastEpisodeViewSet
from .track_views import TrackViewSet
from .folder_views import FolderViewSet

router = DefaultRouter()
router.register(r'libraries', LibraryViewSet, basename='libraries')
router.register(r'libraries/playlists', PlaylistViewSet, basename='libraries/playlists')
router.register(r'libraries/podcasts', PodcastViewSet, basename='libraries/podcasts')

router.register(r'libraries/artists', ArtistViewSet, basename='libraries/artists')
router.register(r'libraries/episodes', PodcastEpisodeViewSet, basename='libraries/episodes')
router.register(r'libraries/tracks', TrackViewSet, basename='libraries/tracks')
router.register(r'libraries/folders', FolderViewSet, basename='libraries/folders')




urlpatterns = [
    path('', include(router.urls)),
]
