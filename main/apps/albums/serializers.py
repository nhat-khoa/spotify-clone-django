from rest_framework import serializers
from .models import Album, AlbumArtist
from apps.artists.serializers import ArtistSerializer
from apps.interactions.models import UserSavedAlbum

class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = '__all__'  # Hoặc có thể liệt kê các trường cụ thể

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserSavedAlbum.objects.filter(user=user, album=obj).exists()
        return False
        


class AlbumArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumArtist
        fields = '__all__'