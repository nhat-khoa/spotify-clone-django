from rest_framework.viewsets import ViewSet
from .models import (
    UserSavedTrack
)
from apps.tracks.models import Track
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class TrackViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def save_track(self, request):
        """Lưu track"""
        track_id = request.data.get('track_id')
        if not track_id:
            return Response({"error": "Track ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        track = get_object_or_404(Track, id=track_id)
       
        UserSavedTrack.objects.get_or_create(user=request.user, track=track)
        return Response({"message": "Track saved", "status": "success"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def remove_saved_track(self, request):
        """Xóa track khỏi danh sách yêu thích"""
        track_id = request.data.get('track_id')
        if not track_id:
            return Response({"error": "Track ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        track = get_object_or_404(Track, id=track_id)
        
        # Xóa track khỏi danh sách yêu thích của user
        deleted_count, _ = UserSavedTrack.objects.filter(user=request.user, track=track).delete()

        # Kiểm tra xem có track nào bị xóa không
        if deleted_count == 0:
            return Response({"message": "Track not found in your saved list", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Track removed", "status": "success"}, status=status.HTTP_200_OK)