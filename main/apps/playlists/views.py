from rest_framework.viewsets import ModelViewSet
from .models import Folder, Playlist, PlaylistTrackPodcast
from .serializers import FolderSerializer, PlaylistSerializer, PlaylistTrackPodcastSerializer

class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

class PlaylistViewSet(ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

class PlaylistTrackPodcastViewSet(ModelViewSet):
    queryset = PlaylistTrackPodcast.objects.all()
    serializer_class = PlaylistTrackPodcastSerializer
