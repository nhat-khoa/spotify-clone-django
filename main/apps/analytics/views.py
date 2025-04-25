from rest_framework_mongoengine import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserStream
from .serializers import UserStreamSerializer
from rest_framework.permissions import AllowAny

class UserStreamViewSet(viewsets.ModelViewSet):
    queryset = UserStream.objects.all()
    serializer_class = UserStreamSerializer
    permission_classes = [AllowAny]
    
    # def get_queryset(self):
    #     # Filter by user_id for security
    #     user_id = self.request.query_params.get('user_id')
    #     if user_id:
    #         return UserStream.objects.filter(user_id=user_id)
    #     return UserStream.objects.none()
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return UserStream.objects(user_id=user_id).order_by('-timestamp')
        return UserStream.objects.none()
