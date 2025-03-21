from rest_framework.viewsets import ModelViewSet
from .models import Track, TrackArtist
from .serializers import TrackSerializer, TrackArtistSerializer

class TrackViewSet(ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class TrackArtistViewSet(ModelViewSet):
    queryset = TrackArtist.objects.all()
    serializer_class = TrackArtistSerializer
