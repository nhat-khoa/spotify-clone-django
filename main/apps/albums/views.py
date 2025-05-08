from rest_framework.viewsets import ModelViewSet
from .models import Album, AlbumArtist
from .serializers import AlbumSerializer, AlbumArtistSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.permissions import IsArtistUser, IsTrackOwner, IsAlbumOwner  # Adjust the import path as necessary

class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated] 
    
    def get_permissions(self):
        match self.action:
            case 'create' :
                permission_classes = [IsAuthenticated, IsArtistUser]
            case 'update' | 'partial_update' | 'destroy' | 'retrieve':
                permission_classes = [IsAuthenticated, IsArtistUser, IsAlbumOwner]
            case _:
                permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Set the artist to the current user (assuming the user is an artist)
        artist = self.request.user.artist_profile
        serializer.save(artist=artist)

class AlbumArtistViewSet(ModelViewSet):
    queryset = AlbumArtist.objects.all()
    serializer_class = AlbumArtistSerializer