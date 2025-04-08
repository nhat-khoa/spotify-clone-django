from rest_framework import serializers
from .models import FavoriteTrack, FavoriteAlbum

class FavoriteTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteTrack
        fields = ['id', 'track', 'created_at']

class FavoriteAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAlbum
        fields = ['id', 'album', 'created_at']
