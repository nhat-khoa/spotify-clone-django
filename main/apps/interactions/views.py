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



class LibraryViewSet(ViewSet):
    
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_library(self, request):
        user = request.user
        
        # Lấy folder và folder con
        folders = Folder.objects.filter(owner=user, parent=None)
        folders_data = FolderSerializer(folders, many=True).data
        
        # Lấy playlist khoong có folder
        playlists = UserFollowedPlaylist.objects.filter(user=user, folder=None)
        playlists = [playlist.playlist for playlist in playlists]
        playlists_data = PlaylistSerializer(playlists, many=True).data

        # Lấy track được lưu
        saved_tracks = UserSavedTrack.objects.filter(user=user).select_related('track')
        saved_tracks_data = TrackSerializer(saved_tracks, many=True).data

        # Lấy artist đang theo dõi
        followed_artists = UserFollowedArtist.objects.filter(user=user).select_related('artist')
        followed_artists_data = ArtistSerializer(followed_artists, many=True).data

        # Lấy episode được lưu
        saved_episodes = UserSavedEpisode.objects.filter(user=user).select_related('episode')
        saved_episodes_data = PodcastEpisodeSerializer(saved_episodes, many=True).data

        # Lấy podcast được lưu
        saved_podcasts = UserFollowedPodcast.objects.filter(user=user).select_related('podcast')
        saved_podcasts_data = PodcastSerializer(saved_podcasts, many=True).data

        return Response({
            "folders": folders_data,
            "playlists": playlists_data,
            "saved_tracks": saved_tracks_data,
            "followed_artists": followed_artists_data,
            "saved_episodes": saved_episodes_data,
            "saved_podcasts": saved_podcasts_data,
            "status": "success"
        }, status=status.HTTP_200_OK)
        
    # ------------------------------ Folder ------------------------------
    @action(detail=False, methods=['post'])
    def add_folder(self, request):
        """Thêm folder"""
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def remove_folder(self, request):
        """Xóa folder"""
        folder_id = request.data.get('folder_id')
        if not folder_id:
            return Response({"error": "Folder ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        Folder.objects.filter(id=folder_id, owner=request.user).delete()
        return Response({"message": "Folder removed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)

    # ------------------------------ Playlist ------------------------------
    

    # ------------------------------ Track ------------------------------
    

    # ------------------------------ Artist ------------------------------
    

    # ------------------------------ Playlist Follow ------------------------------
    
    # ------------------------------ Episode ------------------------------
    

    # ------------------------------ Podcast ------------------------------
    
    
