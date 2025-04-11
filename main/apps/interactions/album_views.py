from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.albums.models import Album
from .models import UserSavedAlbum



class AlbumViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def save_album(self, request):
        """Lưu album"""
        album_id = request.data.get('album_id')
        if not album_id:
            return Response({"error": "Album ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        album = Album.objects.filter(id=album_id).first()
        if not album:
            return Response({"error": "Album not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserSavedAlbum.objects.get_or_create(user=request.user, album=album)
        return Response({"message": "Album saved", "status": "success"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def remove_saved_album(self, request):
        """Xóa album khỏi danh sách lưu"""
        album_id = request.data.get('album_id')
        if not album_id:
            return Response({"error": "Album ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        album = Album.objects.filter(id=album_id).first()
        if not album:
            return Response({"error": "Album not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        UserSavedAlbum.objects.filter(user=request.user, album=album).delete()
        return Response({"message": "Album removed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)