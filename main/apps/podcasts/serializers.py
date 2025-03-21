from rest_framework import serializers
from .models import Podcaster, Podcast, PodcastRate, PodcastEpisode, PodcastEpisodeComment

class PodcasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcaster
        fields = '__all__'

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = '__all__'

class PodcastRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastRate
        fields = '__all__'

class PodcastEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastEpisode
        fields = '__all__'

class PodcastEpisodeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastEpisodeComment
        fields = '__all__'
