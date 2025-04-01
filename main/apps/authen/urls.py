from django.urls import path
from .views import google_login, verify_token, login, register
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path("google-login/", google_login, name="google-login"),
    path("verify/", verify_token, name="verify_token"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
