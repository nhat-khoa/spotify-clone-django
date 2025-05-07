from rest_framework import serializers
from .models import Artist, ArtistImageGallery, ArtistPick
from apps.tracks.models import Track, TrackArtist
from apps.interactions.models import UserSavedTrack
from apps.albums.models import Album


class SimpleAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'  # Hoặc có thể liệt kê các trường cụ thể

class SimpleTrackSerializer(serializers.ModelSerializer):
    album_id = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), required=False)
    is_favorite = serializers.SerializerMethodField()
    album = SimpleAlbumSerializer(read_only=True)  # Assuming you want to show album details
    class Meta:
        model = Track
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True},
            'audio_file_path': {'required': True},
            'artist': {'required': False},  # Assuming artist is required
            'album': {'required': False},  # Assuming album is required
        }
    
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserSavedTrack.objects.filter(user=user, track=obj).exists()
        return False
    
    
class ArtistSerializer(serializers.ModelSerializer):
    tracks = serializers.SerializerMethodField()  # Assuming you want to show artist's tracks
    class Meta:
        model = Artist
        fields = '__all__'  # Hoặc có thể chọn các trường cụ thể
        
    def get_tracks(self, obj):
        # Lấy danh sách các track của artist
        tracks = Track.objects.filter(artist=obj)
        # Sử dụng serializer để chuyển đổi thành định dạng JSON
        serializer = SimpleTrackSerializer(tracks, many=True, context=self.context)
        return serializer.data

class ArtistImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistImageGallery
        fields = '__all__'

class ArtistPickSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistPick
        fields = '__all__'
