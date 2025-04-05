from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LibraryViewSet
router = DefaultRouter()
router.register(r'libraries', LibraryViewSet, basename='user-followed-artist')


urlpatterns = [
    path('', include(router.urls)),
]
