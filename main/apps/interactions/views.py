from rest_framework.viewsets import ViewSet
from .models import (
    UserFollowedArtist, UserFollowedPodcast, UserFollowedPlaylist,
    UserSavedTrack, UserSavedEpisode, Folder, Playlist, UserSavedAlbum
)
from apps.tracks.models import Track
from .serializers import (
    FolderSerializer,
    PlaylistSerializer,
    AlbumInteractionSerializer,
    ArtistInteractionSerializer,
    TrackInteractionSerializer,
    PodcastInteractionSerializer,
)
from apps.tracks.serializers import TrackSerializer
from apps.albums.serializers import AlbumSerializer
from apps.albums.models import Album
from apps.artists.serializers import ArtistSerializer
from apps.artists.models import Artist
from apps.podcasts.serializers import PodcastSerializer, PodcastEpisodeSerializer
from apps.podcasts.models import Podcast
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q
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
        

    
    # get data for home page
    @action(detail=False, methods=['get'])
    def home(self, request):
        """Lấy dữ liệu cho trang chủ"""
        try:
            # Lấy các track phổ biến và premium
            tracks = Track.objects.filter(
                Q(is_premium=False) 
                # Q(is_premium=True, artist__user__premium_expired=True)
            ).order_by('?')[:15]
            
            # Lấy các artist có nhiều track
            artists = Artist.objects.all().order_by('?')[:15]
            
            # Lấy album mới nhất 
            albums = Album.objects.all().order_by('?')[:15]
            
            # Lấy podcast được đánh giá cao
            podcasts = Podcast.objects.all().order_by('?')[:15]

            response_data = {
                "tracks": TrackInteractionSerializer(tracks, many=True, context={'request': request}).data,
                "artists": ArtistInteractionSerializer(artists, many=True, context={'request': request}).data,
                "albums": AlbumInteractionSerializer(albums, 
                                          many=True, context={'request': request}).data,
                "podcasts": PodcastInteractionSerializer(podcasts, many=True, context={'request': request}).data,
                "status": "success"
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": str(e),
                "status": "fail"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get']) 
    def search(self, request):
        """Tìm kiếm track, artist, album, podcast"""
        try:
            search_key = request.query_params.get('q', '').strip()
            if not search_key:
                return Response({
                    "error": "Search key is required",
                    "status": "fail"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Tìm tracks
            tracks = Track.objects.filter(
                Q(title__icontains=search_key) |
                Q(artist__name__icontains=search_key) |
                Q(album__title__icontains=search_key)
            )[:10]

            # Tìm artists 
            artists = Artist.objects.filter(
                Q(name__icontains=search_key) |
                Q(bio__icontains=search_key)
            )[:10]

            # Tìm albums
            albums = Album.objects.filter(
                Q(title__icontains=search_key) |
                Q(artist__name__icontains=search_key) |
                Q(description__icontains=search_key)
            )[:10]

            # Tìm podcasts
            podcasts = Podcast.objects.filter(
                Q(title__icontains=search_key) |
                Q(description__icontains=search_key) |
                Q(podcaster__name__icontains=search_key)
            )[:10]

            response_data = {
                "tracks": TrackInteractionSerializer(
                    tracks, many=True, 
                    context={'request': request}
                ).data,
                "artists": ArtistInteractionSerializer(
                    artists, many=True,
                    context={'request': request}
                ).data,
                "albums": AlbumInteractionSerializer(
                    albums, many=True,
                    context={'request': request}
                ).data,
                "podcasts": PodcastInteractionSerializer(
                    podcasts, many=True,
                    context={'request': request}
                ).data,
                "status": "success"
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": str(e), 
                "status": "fail"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
