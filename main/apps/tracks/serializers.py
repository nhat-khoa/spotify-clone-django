from rest_framework import serializers

from .models import Track, TrackArtist
from apps.artists.serializers import ArtistSerializer
from apps.albums.serializers import AlbumSerializer
from apps.interactions.models import UserSavedTrack
from apps.artists.models import Artist

class TrackSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)  # Assuming you want to show artist details
    album = AlbumSerializer(read_only=True)  # Assuming you want to show album details
    is_favorite = serializers.SerializerMethodField()
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
        
    def validate_audio_file_path(self, value):
        # Validate file extension
        if not value.name.lower().endswith('.mp3'):
            raise serializers.ValidationError('Only MP3 files are allowed')

        # Validate file size (2B)
        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError('File size too large. Maximum size is 20MB')

        return value
    
    def validate_avatar_url(self, value):
        """Validate avatar_url field"""
        if not value or not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError('Only PNG, JPG, or JPEG files are allowed')
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('File size too large. Maximum size is 5MB')
        
        return value
    
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserSavedTrack.objects.filter(user=user, track=obj).exists()
        return False
    
    #  http://127.0.0.1:8000/api/tracks/1c1a114b-c770-43b3-9896-5510c6cf0e44
    def get_audio_stream_url(self, obj):
        # Assuming you have a method to generate the audio stream URL
        return f'http://127.0.0.1:8000/api/tracks/{obj.id}/audio_stream/'  
    


#  track serializer for list view

    

class TrackArtistSerializer(serializers.ModelSerializer):
    # artist = serializers.StringRelatedField()  # or use a nested serializer if needed
    artist = ArtistSerializer(read_only=True )  # Assuming you want to show artist details
    
    class Meta:
        model = TrackArtist
        fields = ('artist', 'role')
