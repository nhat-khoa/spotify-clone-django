from rest_framework import serializers
from .models import Category, PodcastCategory

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

class PodcastCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastCategory
        fields = '__all__'
