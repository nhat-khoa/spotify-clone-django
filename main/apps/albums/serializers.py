from rest_framework import serializers
from .models import Album, AlbumArtist
from apps.artists.serializers import ArtistSerializer
from apps.interactions.models import UserSavedAlbum
from apps.tracks.models import Track


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    tracks = serializers.SerializerMethodField(read_only=True)
    is_favorite = serializers.SerializerMethodField()
    tracks_count = serializers.IntegerField(source='tracks.count', read_only=True)

    class Meta:
        model = Album
        fields = '__all__'  # Hoặc có thể liệt kê các trường cụ thể

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserSavedAlbum.objects.filter(user=user, album=obj).exists()
        return False
    
    def get_tracks(self, obj):
        return Track.objects.filter(album=obj).values()
       
        


class AlbumArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumArtist
        fields = '__all__'