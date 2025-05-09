from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import History
from apps.tracks.models import Track
from .serializers import HistorySerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone

class HistoryViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        histories = History.objects.filter(user=request.user).order_by('-listened_at')
        serializer = HistorySerializer(histories, many=True)
        return Response(serializer.data)

    def create(self, request):
        track_id = request.data.get('track_id')
        track = get_object_or_404(Track, id=track_id)

        # Kiểm tra nếu đã có lịch sử nghe bài hát này
        history, created = History.objects.get_or_create(
            user=request.user,
            track=track,
            defaults={'listened_at': timezone.now()}
        )

        # Nếu đã tồn tại thì cập nhật thời gian nghe
        if not created:
            history.listened_at = timezone.now()
            history.save()

        serializer = HistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
