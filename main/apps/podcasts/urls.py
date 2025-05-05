from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
 PodcastViewSet, 

)

router = DefaultRouter()
router.register(r'podcasts', PodcastViewSet, basename='podcast')


urlpatterns = [
    path('', include(router.urls)),
]
