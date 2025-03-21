from rest_framework import serializers
from .models import Track, TrackArtist

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class TrackArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackArtist
        fields = '__all__'
