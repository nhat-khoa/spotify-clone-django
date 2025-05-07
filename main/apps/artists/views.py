from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Artist, ArtistImageGallery, ArtistPick
from .serializers import ArtistSerializer, ArtistImageGallerySerializer, ArtistPickSerializer,SimpleAlbumSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.core.permissions import IsArtistUser, IsTrackOwner  # Adjust the import path as necessary
from rest_framework.decorators import action
from rest_framework.response import Response

class ArtistViewSet(GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated, IsArtistUser]  # Adjust permissions as needed
    
    def get_permissions(self):
        match self.action:
            case 'create' | 'upload' | 'retrieve' | 'get_tracks':
                permission_classes = [IsAuthenticated, IsArtistUser]
            case 'update' | 'partial_update' | 'destroy' :
                permission_classes = [IsAuthenticated, IsArtistUser, IsTrackOwner]
            case _:  # Mặc định (list, retrieve, get_track_artists, ...)
                permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def get_tracks(self, request, *args, **kwargs):
        artist = request.user.artist_profile
        serializer = self.get_serializer(artist)
        
        return Response({"message": "Get tracks successfully", "result": serializer.data,
                         "status":"success"}, status=200)
        
    @action(detail=False, methods=['get'])
    def get_albums(self, request, *args, **kwargs):
        artist = request.user.artist_profile
        albums = artist.albums.all()
        serializer = SimpleAlbumSerializer(albums, many=True)
        
        return Response({"message": "Get albums successfully", "result": serializer.data,
                         "status":"success"}, status=200)
    

