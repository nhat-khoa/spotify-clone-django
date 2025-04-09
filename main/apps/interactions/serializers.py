from rest_framework import serializers
from .models import (
    UserFollowedArtist, UserFollowedPodcast, UserFollowedPlaylist,
    UserSavedTrack, UserSavedAlbum, UserSavedEpisode, Folder, Playlist,

)
from apps.users.serializers import UserSerializer

class PlaylistSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    user = UserSerializer(read_only=True)
    # avatar_url = serializers.ImageField(use_url=True)
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'description', 
                  'avatar_url', 
                  'is_public', 'likes_count', 
                  'collaborators','items', 'user_id','user']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': False},
            'avatar_url': {'required': False},
            'is_public': {'required': False},
            'likes_count': {'required': False},
            'collaborators': {'required': False},
            'items': {'required': False},
        }
        
    def validate_avatar_url(self, value):
        """Validate avatar_url field"""
        if not value or not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError('Only PNG, JPG, or JPEG files are allowed')
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('File size too large. Maximum size is 5MB')
        
        return value
        
class FolderSerializer(serializers.ModelSerializer):
    """Serializer cho folder (hỗ trợ nested folders)"""
    subfolders = serializers.SerializerMethodField()
    playlists = PlaylistSerializer(many=True, read_only=True)
    
    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent', 'subfolders', 'playlists']    
    
    def get_subfolders(self, obj):
        """Lấy danh sách folder con"""
        subfolders = Folder.objects.filter(parent=obj)
        return FolderSerializer(subfolders, many=True).data    


class UserFollowedArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowedArtist
        fields = '__all__'

class UserFollowedPodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowedPodcast
        fields = '__all__'

class UserFollowedPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowedPlaylist
        fields = '__all__'

class UserSavedTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSavedTrack
        fields = '__all__'

class UserSavedAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSavedAlbum
        fields = '__all__'

class UserSavedEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSavedEpisode
        fields = '__all__'
