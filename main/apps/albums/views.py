from rest_framework.viewsets import ModelViewSet
from .models import Album, AlbumArtist
from .serializers import AlbumSerializer, AlbumArtistSerializer
from rest_framework.permissions import AllowAny

class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny] 

class AlbumArtistViewSet(ModelViewSet):
    queryset = AlbumArtist.objects.all()
    serializer_class = AlbumArtistSerializer