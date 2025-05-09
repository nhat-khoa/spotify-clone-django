from rest_framework import serializers
from .models import Artist, ArtistImageGallery, ArtistPick
from apps.tracks.models import Track, TrackArtist
from apps.interactions.models import UserSavedTrack,UserFollowedArtist
from apps.albums.models import Album


class SimpleAlbumSerializer(serializers.ModelSerializer):
    tracks_count = serializers.IntegerField(source='tracks.count', read_only=True)
    class Meta:
        model = Album
        fields = '__all__'  # Hoặc có thể liệt kê các trường cụ thể

class SimpleTrackSerializer(serializers.ModelSerializer):
    album_id = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), required=False)
    is_favorite = serializers.SerializerMethodField()
    album = SimpleAlbumSerializer(read_only=True)  # Assuming you want to show album details
    audio_stream_url = serializers.SerializerMethodField()
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
   
    def get_audio_stream_url(self, obj):
        # Assuming you have a method to generate the audio stream URL
        return f'http://127.0.0.1:8000/api/tracks/{obj.id}/audio_stream/'  
    
    
class ArtistImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistImageGallery
        fields = '__all__'    
    

class ArtistSerializer(serializers.ModelSerializer):
    tracks = serializers.SerializerMethodField()  # Assuming you want to show artist's tracks
    albums = SimpleAlbumSerializer(many=True, read_only=True)  # Assuming you want to show artist's albums
    gallery_images = ArtistImageGallerySerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()
    followers = serializers.IntegerField(source='followers.count', read_only=True)
    class Meta:
        model = Artist
        fields = '__all__'  # Hoặc có thể chọn các trường cụ thể
        
    def get_tracks(self, obj):
        # Lấy danh sách các track của artist
        tracks = Track.objects.filter(artist=obj)
        # Sử dụng serializer để chuyển đổi thành định dạng JSON
        serializer = SimpleTrackSerializer(tracks, many=True, context=self.context)
        return serializer.data
    
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserFollowedArtist.objects.filter(user=user, artist=obj).exists()
        return False



class ArtistPickSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistPick
        fields = '__all__'
