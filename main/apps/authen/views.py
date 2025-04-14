import os
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate

from apps.users.serializers import UserSerializer

User = get_user_model()

@api_view(["POST"])
@permission_classes([AllowAny])
def google_login(request):
    """Xác thực Google ID Token và tạo JWT"""
    credential = request.data.get("credential")
    if not credential:
        return Response({"error": "credential Google ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Lấy Google Client ID từ biến môi trường
        GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        if not GOOGLE_CLIENT_ID:
            return Response({"error": "Server misconfiguration: GOOGLE_CLIENT_ID not set"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Xác thực token với Google
        id_info = id_token.verify_oauth2_token(credential, requests.Request(), GOOGLE_CLIENT_ID)

        # Lấy thông tin từ token
        email = id_info["email"]
        full_name = id_info.get("name", "")
        avatar_google_url = id_info.get("picture", "")
        
        if avatar_google_url:
            avatar_google_url = avatar_google_url.replace('s96-c', 's400')

        # Kiểm tra xem user đã tồn tại chưa, nếu chưa thì tạo mới
        user, created = User.objects.get_or_create(email=email, defaults={
            "username": email,
            "full_name": full_name,
            "avatar_google_url": avatar_google_url,
            "is_active": True
        })

        # Tạo JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "avatar_google_url": user.avatar_google_url,
                "description": user.description,
                "gender": user.gender,
                "phone": user.phone,
                "age": user.age,
                "date_of_birth": user.date_of_birth,
                "country": user.country,
                "subscription_type": user.subscription_type,
                "avatar_url": user.avatar_url.url if user.avatar_url else "",
                "thumbnail_url": user.thumbnail_url.url if user.thumbnail_url else "",
            }
        }, status=status.HTTP_200_OK)

    except ValueError:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])  # Mở quyền truy cập API
def verify_token(request):
    """Xác thực Access Token từ cookie"""
    # token_str = request.COOKIES.get("access_token")  # Lấy token từ cookie

    # if not token_str:
    #     return Response({"error": "Token không tồn tại"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Lấy token từ header
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({"error": "Header Authorization không tồn tại hoặc không hợp lệ"}, status=401)
        
    token_str = auth_header.split(' ')[1] # cắt chữ Bearer ra khỏi token
    
    if not token_str:
        return Response({"error": "Token không tồn tại"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = AccessToken(token_str)  # Giải mã token
        user = User.objects.get(id=token["user_id"])  # Lấy thông tin user từ token

        return Response({
            "message": "Token hợp lệ",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": "Token không hợp lệ hoặc đã hết hạn"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "avatar_google_url": user.avatar_google_url,
                "avatar_url": user.avatar_url if user.avatar_url else None,
            }
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

