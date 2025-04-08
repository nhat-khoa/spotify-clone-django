from rest_framework import serializers
from apps.favorites.models import FavoriteTrack
from apps.favorites.models import FavoriteAlbum
from apps.tracks.models import Track
from apps.albums.models import Album
from apps.tracks.serializers import TrackSerializer 
from apps.albums.serializers import AlbumSerializer

class FavoriteTrackSerializer(serializers.ModelSerializer):
    track_id = serializers.PrimaryKeyRelatedField(
        queryset=Track.objects.all(),
        source='track',
        write_only=True
    )
    track = TrackSerializer(read_only=True)

    class Meta:
        model = FavoriteTrack
        fields = ['id', 'track', 'track_id', 'created_at']
        read_only_fields = ['id', 'created_at']


class FavoriteAlbumSerializer(serializers.ModelSerializer):
    album_id = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        source='album',
        write_only=True
    )
    album = AlbumSerializer(read_only=True)  

    class Meta:
        model = FavoriteAlbum
        fields = ['id', 'album', 'album_id', 'created_at']
        read_only_fields = ['id', 'created_at']