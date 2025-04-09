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


class TrackViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def save_track(self, request):
        """Lưu track"""
        track_id = request.data.get('track_id')
        if not track_id:
            return Response({"error": "Track ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        track = Track.objects.filter(id=track_id).first()
        if not track:
            return Response({"error": "Track not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserSavedTrack.objects.get_or_create(user=request.user, track=track)
        return Response({"message": "Track saved", "status": "success"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def remove_saved_track(self, request):
        """Xóa track khỏi danh sách lưu"""
        track_id = request.data.get('track_id')
        if not track_id:
            return Response({"error": "Track ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        track = Track.objects.filter(id=track_id).first()
        if not track:
            return Response({"error": "Track not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        UserSavedTrack.objects.filter(user=request.user, track=track).delete()
        return Response({"message": "Track removed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)