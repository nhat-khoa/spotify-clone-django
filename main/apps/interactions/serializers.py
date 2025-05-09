from rest_framework import serializers
from .models import (
    UserFollowedArtist, UserFollowedPodcast, UserFollowedPlaylist,
    UserSavedTrack, UserSavedAlbum, UserSavedEpisode, Folder, Playlist,

)
from apps.users.serializers import UserSerializer
from apps.users.models import User
from apps.tracks.serializers import TrackSerializer
from apps.albums.serializers import AlbumSerializer
from apps.artists.models import Artist  # Import the Artist model
from apps.albums.models import Album  # Import the Album model
from apps.podcasts.models import Podcast, PodcastCategory
from apps.podcasts.serializers import PodcastEpisodeSerializer, SimplePodcasterSerializer
from apps.tracks.models import Track

class PlaylistSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    user = UserSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    collaborators = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'description', 
                  'avatar_url', 
                  'is_public', 'likes_count', 
                  'collaborators','items', 'user_id','user', 'is_favorite',
                  'share_token']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': False},
            'avatar_url': {'required': False},
            'is_public': {'required': False},
            'likes_count': {'required': False},
            'collaborators': {'required': False},
            'items': {'required': False},
            'share_token': {'required': False}
        }
        
    def validate_avatar_url(self, value):
        """Validate avatar_url field"""
        if not value or not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError('Only PNG, JPG, or JPEG files are allowed')
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('File size too large. Maximum size is 5MB')
        
        return value
    
    def get_is_favorite(self, obj):
        """Check if the playlist is favorite"""
        user = self.context['request'].user
        if user.is_authenticated:
            return UserFollowedPlaylist.objects.filter(user=user, playlist=obj).exists()
        return False
    
    def get_likes_count(self, obj):
        """Get the number of likes for the playlist"""
        return UserFollowedPlaylist.objects.filter(playlist=obj).count() - 1
    
    
    def get_collaborators(self, obj):
        """Get the list of collaborators for the playlist"""
        users = []
        for user_id in obj.collaborators:
            user = User.objects.filter(id=user_id).first()
            users.append(user)
        
        return UserSerializer(users, many=True,context=self.context).data if users else []
    
        
class FolderSerializer(serializers.ModelSerializer):
    """Serializer cho folder (hỗ trợ nested folders)"""
    subfolders = serializers.SerializerMethodField(read_only=True)
    playlists = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent','owner', 'subfolders', 'playlists']   
        extra_kwargs = {
            'name': {'required': True},
            'parent': {'required': False},
            'owner': {'required': False},
            'subfolders': {'required': False},
            'playlists': {'required': False},
        }
    
    
    def get_subfolders(self, obj):
        """Lấy danh sách folder con"""
        subfolders = Folder.objects.filter(parent=obj)
        return FolderSerializer(subfolders, many=True, context=self.context).data   
    
    def get_playlists(self, obj):
        """Lấy danh sách playlist trong folder"""
        favorite_playlists = UserFollowedPlaylist.objects.filter(folder=obj)
        playlists = [favorite_playlist.playlist for favorite_playlist in favorite_playlists]
        return PlaylistSerializer(playlists, many=True, context=self.context).data


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
    track = TrackSerializer(read_only=True)
    class Meta:
        model = UserSavedTrack
        fields = '__all__'

class UserSavedAlbumSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)
    class Meta:
        model = UserSavedAlbum
        fields = '__all__'

class UserSavedEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSavedEpisode
        fields = '__all__'
        
        
# artist, podcast, track, album serializer for interactions



class SimpleArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'  # Hoặc có thể chọn các trường cụ thể

class AlbumInteractionSerializer(serializers.ModelSerializer):
    artist = SimpleArtistSerializer(read_only=True)
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
    

    

class ArtistInteractionSerializer(serializers.ModelSerializer):
    albums = AlbumInteractionSerializer(many=True, read_only=True)  # Assuming you want to show artist's albums
    is_favorite = serializers.SerializerMethodField()
    followers = serializers.IntegerField(source='followers.count', read_only=True)
    class Meta:
        model = Artist
        fields = '__all__'  # Hoặc có thể chọn các trường cụ thể
        
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserFollowedArtist.objects.filter(user=user, artist=obj).exists()
        return False


class TrackInteractionSerializer(serializers.ModelSerializer):
    artist = SimpleArtistSerializer(read_only=True)  # Assuming you want to show artist details
    album = AlbumInteractionSerializer(read_only=True)  # Assuming you want to show album details
    is_favorite = serializers.SerializerMethodField()

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
        

class PodcastInteractionSerializer(serializers.ModelSerializer):
    podcaster = SimplePodcasterSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()
    is_rating = serializers.SerializerMethodField()
    rate_average = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    episodes_count = serializers.IntegerField(source='episodes.count', read_only=True)
    class Meta:
        model = Podcast
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True},
            'podcaster': {'required': False}, 

        }
        
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserFollowedPodcast.objects.filter(user=request.user, podcast=obj).exists()
        return False
    
    def get_is_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return any(rating['user_id'] == str(request.user.id) for rating in obj.rate)
        return False
    
    def get_rate_average(self, obj):
        if obj.rate:
            total_rating = sum(rating['rate'] for rating in obj.rate)
            return total_rating / len(obj.rate) if len(obj.rate) > 0 else 0
        return 0
    
    def get_categories(self, obj):
        return PodcastCategory.objects.filter(podcast=obj).select_related('category').values('category__id', 'category__name',)