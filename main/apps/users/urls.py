from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserProfileUpdateView, CheckPremiumStatusView


urlpatterns = [    
    path('profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('profile/check-premium/', CheckPremiumStatusView.as_view(), name='check-premium'),
]