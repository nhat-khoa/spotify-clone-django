from rest_framework.viewsets import ViewSet
from .models import (
    UserFollowedArtist, UserFollowedPodcast, UserFollowedPlaylist,
    UserSavedTrack, UserSavedEpisode, Folder, Playlist
)
from .serializers import (
    FolderSerializer,
    PlaylistSerializer
)
from apps.tracks.serializers import TrackSerializer
from apps.tracks.models import Track
from apps.artists.serializers import ArtistSerializer
from apps.artists.models import Artist
from apps.podcasts.models import PodcastEpisode, Podcast
from apps.podcasts.serializers import PodcastSerializer, PodcastEpisodeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import secrets
import datetime


class ArtistViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def follow_artist(self, request):
        """Theo dõi artist"""
        artist_id = request.data.get('artist_id')
        if not artist_id:
            return Response({"error": "Artist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        artist = Artist.objects.filter(id=artist_id).first()
        if not artist:
            return Response({"error": "Artist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserFollowedArtist.objects.get_or_create(user=request.user, artist=artist)
        return Response({"message": "Artist followed", "status": "success"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def unfollow_artist(self, request):
        """Bỏ theo dõi artist"""
        artist_id = request.data.get('artist_id')
        if not artist_id:
            return Response({"error": "Artist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        artist = Artist.objects.filter(id=artist_id).first()
        if not artist:
            return Response({"error": "Artist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        UserFollowedArtist.objects.filter(user=request.user, artist=artist).delete()
        return Response({"message": "Artist unfollowed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)