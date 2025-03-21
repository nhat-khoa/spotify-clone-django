from rest_framework import serializers
from .models import (
    UserFollowedArtist, UserFollowedPodcast, UserFollowedPlaylist,
    UserSavedTrack, UserSavedAlbum, UserSavedEpisode
)

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
