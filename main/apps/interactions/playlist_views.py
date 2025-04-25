from rest_framework.viewsets import ViewSet
from .models import (
    UserFollowedPlaylist,
    Folder, Playlist
)
from .serializers import (
    PlaylistSerializer,UserFollowedPlaylistSerializer
)
from apps.tracks.models import Track
from apps.podcasts.models import PodcastEpisode
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import secrets
import datetime
from django.db.models import Count
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser



class PlaylistViewSet(ViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    @action(detail=False, methods=['post'])
    def add_playlist(self, request):
        """Thêm playlist"""
        data = request.data.copy()
        if not data.get('name'):
            data['name'] = 'Playlist #' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        serializer = PlaylistSerializer(data=data, context={"request": request})
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

        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        serializer = PlaylistSerializer(playlist, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'])
    def add_playlist_to_folder(self, request):
        """Thêm playlist vào folder"""
        playlist_id = request.data.get('playlist_id')
        folder_id = request.data.get('parent_folder_id')
        if not playlist_id or not folder_id:
            return Response({"error": "Playlist ID and Folder ID are required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = get_object_or_404(Playlist, id=playlist_id, is_public=True)
        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
        ufp = UserFollowedPlaylist.objects.get_or_create(user=request.user, playlist=playlist)
        ufp[0].folder = folder
        ufp[0].save()
        return Response({"message": "Playlist added to folder", "status": "success"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['put'])
    def remove_playlist_from_folder(self, request):
        """Xóa playlist khỏi folder"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID are required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        UserFollowedPlaylist.objects.filter(user=request.user, playlist=playlist).update(folder=None)
        return Response({"message": "Playlist removed from folder", "status": "success"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_playlists(self, request):
        """Lấy danh sách playlist"""
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_playlist_by_id(self, request):
        """Lấy thông tin playlist"""
        playlist_id = request.query_params.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = get_object_or_404(Playlist, id=playlist_id, is_public=True)
        # Count số người theo dõi
        followers_count = UserFollowedPlaylist.objects.filter(playlist=playlist).count()
        serializer = PlaylistSerializer(playlist, context={"request": request})
        data = serializer.data
        data['followers_count'] = followers_count
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'])
    def remove_playlist(self, request):
        """Xóa playlist"""
        playlist_id = request.data.get('playlist_id')
        print(playlist_id)
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        get_object_or_404(Playlist, id=playlist_id, user=request.user).delete()
        return Response({"message": "Playlist removed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])
    def follow_playlist(self, request):
        """Theo dõi playlist"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = get_object_or_404(Playlist, id=playlist_id)
        if playlist.user == request.user:
            return Response({"error": "You cannot follow your own playlist", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        UserFollowedPlaylist.objects.get_or_create(user=request.user, playlist=playlist)
        return Response({"message": "Playlist followed", "status": "success",
                         "result": PlaylistSerializer(playlist, context={"request": request}).data}, 
                        status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['post'])
    def unfollow_playlist(self, request):
        """Bỏ theo dõi playlist"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        playlist = get_object_or_404(Playlist, id=playlist_id)
        followed_playlist = get_object_or_404(UserFollowedPlaylist, user=request.user, playlist=playlist)
        if followed_playlist.playlist.user == request.user:
            return Response({"error": "You cannot unfollow your playlist", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        followed_playlist.delete()
        return Response({"message": "Playlist unfollowed", "status": "success",
                         "result": PlaylistSerializer(playlist, context={"request": request}).data},
                        status=status.HTTP_200_OK)
    
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
        
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
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
            "item_image":   request.build_absolute_uri(item.album.avatar_url.url)
                            if item_type == 'track' and item.album and item.album.avatar_url 
                            else request.build_absolute_uri(item.cover_art_image_url.url) 
                            if item_type == 'podcast_episode' and item.cover_art_image_url 
                            else '',
            "item_duration_ms": item.duration_ms,
            "created_at": datetime.datetime.now().isoformat(),
        })
        
        playlist.save()
        return Response({"message": "Item added to playlist", "status": "success",
                         "result": playlist.items }, status=status.HTTP_201_CREATED)
        
        
    @action(detail=False, methods=['put'])
    def change_item_order(self, request):
        """Thay đổi thứ tự item trong playlist"""
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
        targed_items = [item for item in items if item['uid'] == from_uid]
        if not targed_items:
            return Response({"error": "Items does not change", "status": "fail"}, status=status.HTTP_200_OK)
        
        targed_item = targed_items[0]
        
        index_inserting = items.index(targed_item) + 1 if move_type == 'after' else items.index(targed_item)
        items = items[:index_inserting] + moving_items + items[index_inserting:]
        playlist.items = items
        playlist.save()
        return Response({"message": "Item order changed", "status": "success",
                         "result": playlist.items }, status=status.HTTP_200_OK)
        
        
    @action(detail=False, methods=['put'])
    def change_item_order2(self, request):
        """Thay đổi thứ tự item trong playlist"""
        playlist_id = request.data.get('playlist_id')
        uids = request.data.get('uids')
        
        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        if not playlist or not uids:
            return Response({"error": "Playlist not found or uids are None", 
                             "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        new_items = []
        for index, uid in enumerate(uids):
            new_items.append([item for item in playlist.items if item['uid'] == uid][0])
           
        playlist.items = new_items
        playlist.save()
        return Response({"message": "Item order changed", "status": "success",
                         "result": playlist.items }, status=status.HTTP_200_OK)    
    
        
    @action(detail=False, methods=['post'])
    def remove_item_from_playlist(self, request):
        """Xóa item khỏi playlist"""
        playlist_id = request.data.get('playlist_id')
        item_uid = request.data.get('item_uid')
        
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        
        items = playlist.items
        items = [item for item in items if item['uid'] != item_uid]
        playlist.items = items
        playlist.save()
        return Response({"message": "Item removed from playlist", "status": "success",
                         "result": playlist.items }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='my-public-playlists')
    def my_public_playlists(self, request):
        """Lấy danh sách playlist công khai của chính mình"""
        playlists = Playlist.objects.filter(user=request.user, is_public=True)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)