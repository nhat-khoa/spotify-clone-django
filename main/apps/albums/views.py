from rest_framework.viewsets import ModelViewSet
from .models import Album, AlbumArtist
from .serializers import AlbumSerializer, AlbumArtistSerializer

class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumArtistViewSet(ModelViewSet):
    queryset = AlbumArtist.objects.all()
    serializer_class = AlbumArtistSerializer