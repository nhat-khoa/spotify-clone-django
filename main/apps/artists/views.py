from rest_framework.viewsets import ModelViewSet
from .models import Artist, ArtistImageGallery, ArtistPick
from .serializers import ArtistSerializer, ArtistImageGallerySerializer, ArtistPickSerializer
from rest_framework.permissions import AllowAny


class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]  # Adjust permissions as needed

class ArtistImageGalleryViewSet(ModelViewSet):
    queryset = ArtistImageGallery.objects.all()
    serializer_class = ArtistImageGallerySerializer

class ArtistPickViewSet(ModelViewSet):
    queryset = ArtistPick.objects.all()
    serializer_class = ArtistPickSerializer
