from rest_framework.viewsets import ModelViewSet
from .models import Podcaster, Podcast, PodcastRate, PodcastEpisode, PodcastEpisodeComment
from .serializers import (
    PodcasterSerializer, PodcastSerializer, PodcastRateSerializer,
    PodcastEpisodeSerializer, PodcastEpisodeCommentSerializer
)

class PodcasterViewSet(ModelViewSet):
    queryset = Podcaster.objects.all()
    serializer_class = PodcasterSerializer

class PodcastViewSet(ModelViewSet):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

class PodcastRateViewSet(ModelViewSet):
    queryset = PodcastRate.objects.all()
    serializer_class = PodcastRateSerializer

class PodcastEpisodeViewSet(ModelViewSet):
    queryset = PodcastEpisode.objects.all()
    serializer_class = PodcastEpisodeSerializer

class PodcastEpisodeCommentViewSet(ModelViewSet):
    queryset = PodcastEpisodeComment.objects.all()
    serializer_class = PodcastEpisodeCommentSerializer
