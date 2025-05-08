from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from .models import Podcaster, Podcast,PodcastEpisode
from .serializers import (
    PodcasterSerializer, PodcastSerializer,
    PodcastEpisodeSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsPodcasterUser, IsPodcastOwner
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class PodcastViewSet(GenericViewSet,
                     mixins.ListModelMixin,mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,mixins.DestroyModelMixin,
                     ):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    
    def get_permissions(self):
        match self.action:
            case 'create' | 'upload' | 'get_podcasts':
                permission_classes = [IsAuthenticated, IsPodcasterUser]
            case 'update' | 'partial_update' | 'destroy':
                permission_classes = [IsAuthenticated, IsPodcasterUser, IsPodcastOwner]
            case _:  # Mặc định (list, retrieve, get_track_artists, ...)
                permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def get_podcasts(self, request):
        """Lấy danh sách podcast"""
        podcasts = Podcast.objects.all().filter(podcaster=request.user.podcaster_profile)
        serializer = self.get_serializer(podcasts, many=True)
        return Response({"message": "Get podcasts successfully", "result": serializer.data,
                         "status":"success"}, status=200)
    
    
    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}   
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(podcaster=request.user.podcaster_profile )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def create_episode(self, request, pk=None):
        podcast = self.get_object()
        serializer = PodcastEpisodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(podcast=podcast)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def rate_podcast(self, request, pk=None):
        """Đánh giá podcast"""
        podcast = Podcast.objects.get(id=pk)
        rating = request.data.get('rating')
        if not rating:
            return Response({"error": "Rating is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not podcast.rate:
            podcast.rate = []
        
        if rating < 1 or rating > 5:
            return Response({"error": "Rating must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)
        
        for r in podcast.rate:
            if r['user_id'] == str(request.user.id):
                r['rate'] = rating
                break
        else:
            podcast.rate.append({
                "user_id": str(request.user.id),
                "rate": rating
            })
        
        podcast.save()
        return Response({"message": "Rating added successfully",
                        "result": PodcastSerializer(podcast, context={'request': request}).data,
                        "status": "success",
                         },
                        status=status.HTTP_201_CREATED)
        
    
    @action(detail=False, methods=['get'])
    def get_episode_details(self, request):
        """Lấy thông tin chi tiết của một tập podcast"""
        pk = request.query_params.get('episode_id')
        if not pk:
            return Response({"error": "episode_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        episode = PodcastEpisode.objects.get(id=pk)
        serializer = PodcastEpisodeSerializer(episode, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class PodcasterViewSet(GenericViewSet):
    queryset = Podcaster.objects.all()
    serializer_class = PodcasterSerializer
    
    def get_permissions(self):
        match self.action:
            case 'create' | 'update' | 'partial_update' | 'destroy':
                permission_classes = [IsAuthenticated, IsPodcasterUser]
            case _:  # Mặc định (list, retrieve, get_track_artists, ...)
                permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


