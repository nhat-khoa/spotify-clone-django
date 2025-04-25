from rest_framework.viewsets import ViewSet

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

class ArtistViewSet(ViewSet):
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
        return Response({"message": "Artist followed", "status": "success"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def unfollow_artist(self, request):
        """Bỏ theo dõi artist"""
        artist_id = request.data.get('artist_id')
        if not artist_id:
            return Response({"error": "Artist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        artist = get_object_or_404(Artist, id=artist_id)        
        get_object_or_404(UserFollowedArtist, user=request.user, artist=artist).delete()
        return Response({"message": "Artist unfollowed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], url_path='my-followed')
    def my_followed_artists(self, request):
        followed = UserFollowedArtist.objects.filter(user=request.user).select_related('artist')
        artists = [f.artist for f in followed]
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)