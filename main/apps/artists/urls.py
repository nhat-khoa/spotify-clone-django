from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet, ArtistImageGalleryViewSet, ArtistPickViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'artist-gallery', ArtistImageGalleryViewSet, basename='artist-gallery')
router.register(r'artist-picks', ArtistPickViewSet, basename='artist-picks')

urlpatterns = [
    path('', include(router.urls)),
]