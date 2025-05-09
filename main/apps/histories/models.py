from django.db import models
from apps.core.models import BaseModel
from apps.users.models import User
from apps.tracks.models import Track

class History(BaseModel):
    """Lưu lịch sử nghe bài hát"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listened_histories')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='track_histories')
    listened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} listened {self.track} at {self.listened_at}"
