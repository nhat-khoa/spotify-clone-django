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
        playlists = UserFollowedPlaylist.objects.filter(user=user, folder=None).select_related('playlist')
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
    @action(detail=False, methods=['post'])
    def add_playlist(self, request):
        """Thêm playlist"""
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            UserFollowedPlaylist.objects.create(user=request.user, playlist=serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'])
    def update_playlist(self, request):
        """Cập nhật playlist"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'])
    def add_playlist_to_folder(self, request):
        """Thêm playlist vào folder"""
        playlist_id = request.data.get('playlist_id')
        folder_id = request.data.get('folder_id')
        if not playlist_id or not folder_id:
            return Response({"error": "Playlist ID and Folder ID are required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        folder = Folder.objects.filter(id=folder_id, owner=request.user).first()
        if not playlist or not folder:
            return Response({"error": "Playlist or Folder not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserFollowedPlaylist.objects.filter(user=request.user, playlist=playlist).update(folder=folder)
        return Response({"message": "Playlist added to folder", "status": "success"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['put'])
    def remove_playlist_from_folder(self, request):
        """Xóa playlist khỏi folder"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID are required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserFollowedPlaylist.objects.filter(user=request.user, playlist=playlist).update(folder=None)
        return Response({"message": "Playlist removed from folder", "status": "success"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_playlists(self, request):
        """Lấy danh sách playlist"""
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'])
    def remove_playlist(self, request):
        """Xóa playlist"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        Playlist.objects.filter(id=playlist_id, user=request.user).delete()
        return Response({"message": "Playlist removed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)

    # ------------------------------ Track ------------------------------
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

    # ------------------------------ Artist ------------------------------
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

    # ------------------------------ Playlist Follow ------------------------------
    @action(detail=True, methods=['post'])
    def follow_playlist(self, request, pk=None):
        """Theo dõi playlist"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = Playlist.objects.filter(id=playlist_id).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserFollowedPlaylist.objects.get_or_create(user=request.user, playlist=playlist)
        return Response({"message": "Playlist followed", "status": "success"}, status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=['delete'])
    def unfollow_playlist(self, request):
        """Bỏ theo dõi playlist"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        playlist = Playlist.objects.filter(id=playlist_id).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        followed_playlist = UserFollowedPlaylist.objects.filter(user=request.user, playlist=playlist)
        if followed_playlist.user == request.user:
            return Response({"error": "You cannot unfollow your playlist", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        followed_playlist.delete()
        return Response({"message": "Playlist unfollowed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)

    # ------------------------------ Episode ------------------------------
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

    # ------------------------------ Podcast ------------------------------
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
    
    # ------------------------------ Playlist Items ------------------------------
    @action(detail=False, methods=['post'])
    def add_item_to_playlist(self, request):
        """Thêm item vào playlist"""
        playlist_id = request.data.get('playlist_id')
        item_type = request.data.get('item_type')
        item_id = request.data.get('item_id')
        item = None
        if item_type == 'track':
            item = get_object_or_404(Track, id=item_id)
        elif item_type == 'podcast_episode':
            item = get_object_or_404(PodcastEpisode, id=item_id)
        
        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        if not playlist.items:
            playlist.items = []
        
        playlist.items.append({
            "uid": secrets.token_hex(8),
            "item_type": item_type,
            "item_id": str(item.id),
            "item_name": item.title,
            "owner_id": str(item.artist.id) if item_type == 'track' else str(item.podcast.podcaster.id),
            "owner_name": item.artist.name if item_type == 'track' else item.podcast.podcaster.name,
            "album_or_podcast": item.album.title if item_type == 'track' else item.podcast.title,
            "album_or_podcast_id": str(item.album.id) if item_type == 'track' else str(item.podcast.id),
            "item_image":   item.album.avatar_url.url
                            if item_type == 'track' and item.album and item.album.avatar_url 
                            else item.cover_art_image_url.url 
                            if item_type == 'podcast_episode' and item.cover_art_image_url 
                            else '',
            "item_duration_ms": item.duration_ms,
            "created_at": datetime.datetime.now().isoformat(),
        })
        
        playlist.save()
        return Response({"message": "Item added to playlist", "status": "success",
                         "data": playlist.items[-1] }, status=status.HTTP_201_CREATED)
        
        
    @action(detail=False, methods=['put'])
    def change_item_order(self, request):
        """Thay đổi thứ tự item trong playlist"""
        user = request.user
        playlist_id = request.data.get('playlist_id')
        uids = request.data.get('uids', [])
        move_type = request.data.get('move_type')
        from_uid = request.data.get('from_uid')
        
        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        items = playlist.items
        moving_items = [item for item in items if item['uid'] in uids]
        items = [item for item in items if item['uid'] not in uids]
        targed_item = [item for item in items if item['uid'] == from_uid][0]
        index_inserting = items.index(targed_item) + 1 if move_type == 'after' else items.index(targed_item)
        items = items[:index_inserting] + moving_items + items[index_inserting:]
        playlist.items = items
        playlist.save()
        return Response({"message": "Item order changed", "status": "success",
                         "data": playlist.items }, status=status.HTTP_200_OK)
            

        
        
        


            
    
