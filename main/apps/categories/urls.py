from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PodcastCategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'podcast-categories', PodcastCategoryViewSet, basename='podcast-category')

urlpatterns = [
    path('', include(router.urls)),
]
