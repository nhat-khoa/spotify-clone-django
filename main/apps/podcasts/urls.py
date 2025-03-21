from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PodcasterViewSet, PodcastViewSet, PodcastRateViewSet,
    PodcastEpisodeViewSet, PodcastEpisodeCommentViewSet
)

router = DefaultRouter()
router.register(r'podcasters', PodcasterViewSet, basename='podcaster')
router.register(r'podcasts', PodcastViewSet, basename='podcast')
router.register(r'podcast-rates', PodcastRateViewSet, basename='podcast-rate')
router.register(r'podcast-episodes', PodcastEpisodeViewSet, basename='podcast-episode')
router.register(r'podcast-comments', PodcastEpisodeCommentViewSet, basename='podcast-comment')

urlpatterns = [
    path('', include(router.urls)),
]
