from rest_framework.viewsets import ViewSet, GenericViewSet

from apps.artists.serializers import ArtistSerializer
from .models import (
    UserFollowedArtist,
)
from apps.artists.models import Artist
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class ArtistViewSet(GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def follow_artist(self, request):
        """Theo dõi artist"""
        artist_id = request.data.get('artist_id')
        if not artist_id:
            return Response({"error": "Artist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        artist = get_object_or_404(Artist, id=artist_id)
        UserFollowedArtist.objects.get_or_create(user=request.user, artist=artist)
        return Response({"message": "Artist followed", "status": "success",
                         "result": ArtistSerializer(artist, context={'request': request}).data
                         }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def unfollow_artist(self, request):
        """Bỏ theo dõi artist"""
        artist_id = request.data.get('artist_id')
        if not artist_id:
            return Response({"error": "Artist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        artist = get_object_or_404(Artist, id=artist_id)        
        UserFollowedArtist.objects.filter(user=request.user, artist=artist).delete()
        return Response({"message": "Artist unfollowed", "status": "success",
                         "result": ArtistSerializer(artist, context={'request': request}).data
                         },
                        status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='my-followed')
    def my_followed_artists(self, request):
        followed = UserFollowedArtist.objects.filter(user=request.user).select_related('artist')
        artists = [f.artist for f in followed]
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def get_artist(self, request, *args, **kwargs):
        """Lấy thông tin artist"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"message": "Get artist successfully", "result": serializer.data,
                         "status":"success"}, status=200)