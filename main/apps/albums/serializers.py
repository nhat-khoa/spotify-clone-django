from rest_framework import serializers
from .models import Album, AlbumArtist
from apps.artists.serializers import ArtistSerializer

class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  
    class Meta:
        model = Album
        fields = '__all__'  # Hoặc có thể liệt kê các trường cụ thể
        


class AlbumArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumArtist
        fields = '__all__'