from django.urls import path
from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserProfileUpdateView, CheckPremiumStatusView, UserViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [    
    path('profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('profile/check-premium/', CheckPremiumStatusView.as_view(), name='check-premium'),
    path('', include(router.urls)),
]