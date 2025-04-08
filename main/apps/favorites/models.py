from django.db import models
from apps.core.models import BaseModel  # giả sử bạn đặt BaseModel trong apps.core.models

class FavoriteTrack(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='favorite_tracks')
    track = models.ForeignKey('tracks.Track', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'track')


class FavoriteAlbum(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='favorite_albums')
    album = models.ForeignKey('albums.Album', on_delete=models.CASCADE)  

    class Meta:
        unique_together = ('user', 'album')
