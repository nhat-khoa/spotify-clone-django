from rest_framework import serializers
from .models import Artist, ArtistImageGallery, ArtistPick

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'  # Hoặc có thể chọn các trường cụ thể

class ArtistImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistImageGallery
        fields = '__all__'

class ArtistPickSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistPick
        fields = '__all__'
