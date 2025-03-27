from django.urls import path
from .views import google_login, verify_token

urlpatterns = [
    path("google-login/", google_login, name="google-login"),
    path("verify/", verify_token, name="verify_token"),
]
