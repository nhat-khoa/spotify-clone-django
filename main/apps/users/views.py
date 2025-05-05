from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer
import jwt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.utils import timezone
from .models import User
from .serializers import UserProfileSerializer
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Cho phép upload file

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)  # partial=True cho phép cập nhật 1 phần
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CheckPremiumStatusView(APIView):
    permission_classes = [IsAuthenticated]  # Yêu cầu đăng nhập

    def get(self, request, *args, **kwargs):
        user = request.user
        is_premium = user.premium_expired and user.premium_expired > timezone.now()
        return Response({
            "is_premium": is_premium,
            "premium_expired": user.premium_expired
        }, status=status.HTTP_200_OK)
        
class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    