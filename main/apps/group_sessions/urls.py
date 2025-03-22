from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupSessionViewSet

router = DefaultRouter()
router.register(r"group_sessions", GroupSessionViewSet, basename="group_session")

urlpatterns = [
    path("", include(router.urls)),
]