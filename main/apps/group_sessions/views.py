from rest_framework_mongoengine import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import GroupSession
from .serializers import GroupSessionSerializer
import datetime
class GroupSessionViewSet(viewsets.ModelViewSet):
    queryset = GroupSession.objects.all()
    serializer_class = GroupSessionSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def get_all(self, request):
        sessions = GroupSession.objects.all()
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def end_session(self, request, id=None):
        session = self.get_object()
        session.status = 'ended'
        session.is_active = False
        session.ended_at = datetime.datetime.now()
        session.save()
        serializer = self.get_serializer(session)
        return Response(serializer.data)