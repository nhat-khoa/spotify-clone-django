from rest_framework.viewsets import ViewSet
from .models import (
    UserFollowedArtist, UserFollowedPodcast, UserFollowedPlaylist,
    UserSavedTrack, UserSavedEpisode, Folder, Playlist, UserSavedAlbum
)
from .serializers import (
    FolderSerializer,
    PlaylistSerializer
)
from apps.tracks.serializers import TrackSerializer
from apps.albums.serializers import AlbumSerializer
from apps.artists.serializers import ArtistSerializer
from apps.podcasts.serializers import PodcastSerializer, PodcastEpisodeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSavedTrackSerializer
from .serializers import UserSavedAlbumSerializer

class LibraryViewSet(ViewSet):
    
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_library(self, request):
        user = request.user
        
        # # Lấy folder và folder con
        folders = Folder.objects.filter(owner=user, parent=None)
        folders_data = FolderSerializer(folders, many=True, context={"request": request}).data
        
        # Lấy playlist khoong có folder
        playlists = Playlist.objects.filter(followers__user=user, followers__folder=None)
        playlists_data = PlaylistSerializer(playlists, many=True, context={"request": request}).data

        # Lấy track được lưu
        saved_tracks = UserSavedTrack.objects.filter(user=user).select_related('track')
        saved_tracks = [saved_track.track for saved_track in saved_tracks]
        saved_tracks_data = TrackSerializer(saved_tracks, many=True, context={"request": request}).data

        # Lấy artist đang theo dõi
        followed_artists = UserFollowedArtist.objects.filter(user=user).select_related('artist')
        followed_artists = [followed_artist.artist for followed_artist in followed_artists]
        followed_artists_data = ArtistSerializer(followed_artists, many=True, context={"request": request}).data

        # Lấy episode được lưu
        saved_episodes = UserSavedEpisode.objects.filter(user=user).select_related('episode')
        saved_episodes = [saved_episode.episode for saved_episode in saved_episodes]
        saved_episodes_data = PodcastEpisodeSerializer(saved_episodes, many=True, context={"request": request}).data

        # album
        saved_albums = UserSavedAlbum.objects.filter(user=user).select_related('album')
        saved_albums = [saved_album.album for saved_album in saved_albums]
        saved_albums_data = AlbumSerializer(saved_albums, many=True, context={"request": request}).data
        
        # Lấy podcast được lưu
        followed_podcasts = UserFollowedPodcast.objects.filter(user=user).select_related('podcast')
        followed_podcasts = [followed_podcast.podcast for followed_podcast in followed_podcasts]    
        followed_podcasts_data = PodcastSerializer(followed_podcasts, many=True, context={"request": request}).data

        return Response({
            "folders": folders_data,
            "playlists": playlists_data,
            "saved_tracks": saved_tracks_data,
            "saved_albums": saved_albums_data,
            "followed_artists": followed_artists_data,
            "saved_albums": saved_albums_data,
            "saved_episodes": saved_episodes_data,
            "saved_podcasts": followed_podcasts_data,
            "status": "success"
        }, status=status.HTTP_200_OK)
        
    # ------------------------------ Folder ------------------------------
    

    # ------------------------------ Playlist ------------------------------
    

    # ------------------------------ Track ------------------------------
    

    # ------------------------------ Artist ------------------------------
    

    # ------------------------------ Playlist Follow ------------------------------
    
    # ------------------------------ Episode ------------------------------
    

    # ------------------------------ Podcast ------------------------------
    
    
