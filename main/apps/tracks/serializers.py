from rest_framework import serializers

from apps.artists.serializers import ArtistSerializer
from .models import Track, TrackArtist
from apps.artists.models import Artist

class TrackSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())  # Nhận UUID
    class Meta:
        model = Track
        fields = '__all__'

class TrackArtistSerializer(serializers.ModelSerializer):
    # artist = serializers.StringRelatedField()  # or use a nested serializer if needed
    artist = ArtistSerializer()
    
    class Meta:
        model = TrackArtist
        fields = '__all__'
