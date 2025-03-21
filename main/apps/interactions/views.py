from rest_framework.viewsets import ModelViewSet
from .models import (
    UserFollowedArtist, UserFollowedPodcast, UserFollowedPlaylist,
    UserSavedTrack, UserSavedAlbum, UserSavedEpisode
)
from .serializers import (
    UserFollowedArtistSerializer, UserFollowedPodcastSerializer, UserFollowedPlaylistSerializer,
    UserSavedTrackSerializer, UserSavedAlbumSerializer, UserSavedEpisodeSerializer
)

class UserFollowedArtistViewSet(ModelViewSet):
    queryset = UserFollowedArtist.objects.all()
    serializer_class = UserFollowedArtistSerializer

class UserFollowedPodcastViewSet(ModelViewSet):
    queryset = UserFollowedPodcast.objects.all()
    serializer_class = UserFollowedPodcastSerializer

class UserFollowedPlaylistViewSet(ModelViewSet):
    queryset = UserFollowedPlaylist.objects.all()
    serializer_class = UserFollowedPlaylistSerializer

class UserSavedTrackViewSet(ModelViewSet):
    queryset = UserSavedTrack.objects.all()
    serializer_class = UserSavedTrackSerializer

class UserSavedAlbumViewSet(ModelViewSet):
    queryset = UserSavedAlbum.objects.all()
    serializer_class = UserSavedAlbumSerializer

class UserSavedEpisodeViewSet(ModelViewSet):
    queryset = UserSavedEpisode.objects.all()
    serializer_class = UserSavedEpisodeSerializer
