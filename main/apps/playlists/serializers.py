from rest_framework import serializers
from .models import Folder, Playlist, PlaylistTrackPodcast

class FolderSerializer(serializers.ModelSerializer):
    subfolders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'

class PlaylistTrackPodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistTrackPodcast
        fields = '__all__'
