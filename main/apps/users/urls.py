from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserProfileUpdateView


urlpatterns = [    
    path('profile/', UserProfileUpdateView.as_view(), name='update-profile'),
]