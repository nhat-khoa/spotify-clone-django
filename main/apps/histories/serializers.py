from rest_framework import serializers

from apps.artists.serializers import ArtistSerializer
from apps.tracks.serializers import TrackSerializer
from .models import History

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
        read_only_fields = ['user', 'listened_at']
# class HistoryTrackSerializer(serializers.ModelSerializer):
#     track = TrackSerializer()
#     artist = ArtistSerializer(read_only=True)  # Assuming you want to show artist details
#     album = AlbumSerializer(read_only=True)  # Assuming you want to show album details
#     is_favorite = serializers.SerializerMethodField()

#     class Meta:
#         model = History
#         fields = ['track', 'listened_at']