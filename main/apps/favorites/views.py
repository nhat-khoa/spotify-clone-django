from rest_framework.viewsets import ModelViewSet
from .models import FavoriteTrack, FavoriteAlbum
from .serializers import FavoriteTrackSerializer, FavoriteAlbumSerializer

class FavoriteTrackViewSet(ModelViewSet):
    serializer_class = FavoriteTrackSerializer

    def get_queryset(self):
        return FavoriteTrack.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteAlbumViewSet(ModelViewSet):
    serializer_class = FavoriteAlbumSerializer

    def get_queryset(self):
        return FavoriteAlbum.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
