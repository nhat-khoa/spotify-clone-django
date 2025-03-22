from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  UserStreamViewSet

router = DefaultRouter()
router.register(r"user_streams", UserStreamViewSet, basename="user_stream")

urlpatterns = [
    path("", include(router.urls)),
]