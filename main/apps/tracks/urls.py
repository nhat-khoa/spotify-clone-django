from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackViewSet, TrackArtistViewSet

router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename='track')
router.register(r'track-artists', TrackArtistViewSet, basename='track-artist')

urlpatterns = [
    path('', include(router.urls)),
]
