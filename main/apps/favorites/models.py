from django.db import models

class FavoriteTrack(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='favorite_tracks')
    track = models.ForeignKey('tracks.Track', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')


class FavoriteAlbum(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='favorite_albums')
    album = models.ForeignKey('tracks.Track', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'album')
