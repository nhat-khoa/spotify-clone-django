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


class PodcastViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def follow_podcast(self, request):
        """Theo dõi podcast"""
        podcast_id = request.data.get('podcast_id')
        if not podcast_id:
            return Response({"error": "Podcast ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        podcast = Podcast.objects.filter(id=podcast_id).first()
        if not podcast:
            return Response({"error": "Podcast not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserFollowedPodcast.objects.get_or_create(user=request.user, podcast=podcast)
        return Response({"message": "Podcast followed", "status": "success"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def unfollow_podcast(self, request):
        """Bỏ theo dõi podcast"""
        podcast_id = request.data.get('podcast_id')
        if not podcast_id:
            return Response({"error": "Podcast ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        podcast = Podcast.objects.filter(id=podcast_id).first()
        if not podcast:
            return Response({"error": "Podcast not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserFollowedPodcast.objects.filter(user=request.user, podcast=podcast).delete()
        return Response({"message": "Podcast unfollowed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)