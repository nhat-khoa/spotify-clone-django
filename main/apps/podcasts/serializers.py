from rest_framework import serializers
from .models import Podcaster, Podcast, PodcastEpisode, PodcastCategory
from apps.interactions.models import UserFollowedPodcast, UserSavedEpisode


class PodcasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcaster
        fields = '__all__'
    
# Podcast episode serializer
class SimplePodcasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcaster
        fields = '__all__'

class SimplePodcastSerializer(serializers.ModelSerializer):
    podcaster = SimplePodcasterSerializer(read_only=True)
    class Meta:
        model = Podcast
        fields = '__all__'

class PodcastEpisodeSerializer(serializers.ModelSerializer):
    podcast = SimplePodcastSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()
    class Meta:
        model = PodcastEpisode
        fields = '__all__'
        
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserSavedEpisode.objects.filter(user=request.user,episode=obj).exists()
        return False
    
# Podcast serializer
class SimplePodcasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcaster
        fields = '__all__'


class PodcastSerializer(serializers.ModelSerializer):
    episodes = PodcastEpisodeSerializer(many=True, read_only=True)
    podcaster = SimplePodcasterSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()
    is_rating = serializers.SerializerMethodField()
    rate_average = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
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