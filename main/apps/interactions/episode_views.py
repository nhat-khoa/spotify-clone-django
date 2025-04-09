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


class PodcastEpisodeViewSet(ViewSet):
        
    permission_classes = [IsAuthenticated]
        
    @action(detail=False, methods=['post'])
    def save_episode(self, request):
        """Lưu episode"""
        episode_id = request.data.get('episode_id')
        if not episode_id:
            return Response({"error": "Episode ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        episode = PodcastEpisode.objects.filter(id=episode_id).first()
        if not episode:
            return Response({"error": "Episode not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserSavedEpisode.objects.get_or_create(user=request.user, episode=episode)
        return Response({"message": "Episode saved", "status": "success"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def remove_saved_episode(self, request):
        """Xóa episode khỏi danh sách lưu"""
        episode_id = request.data.get('episode_id')
        if not episode_id:
            return Response({"error": "Episode ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        episode = PodcastEpisode.objects.filter(id=episode_id).first()
        if not episode:
            return Response({"error": "Episode not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserSavedEpisode.objects.filter(user=request.user, episode=episode).delete()
        return Response({"message": "Episode removed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)
