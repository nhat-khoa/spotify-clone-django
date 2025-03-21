from django.db import models
from apps.core.models import BaseModel  # Import BaseModel từ core
from apps.core.utils import generate_unique_filename

class Folder(BaseModel):
    """Model for folders to organize playlists"""
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    
    def __str__(self):
        return self.name


class Playlist(BaseModel):
    """Model for playlists"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_playlists')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    avatar_url = models.ImageField(upload_to=generate_unique_filename)
    is_public = models.BooleanField(default=True)
    likes_count = models.IntegerField(default=0)
    collaborators = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return self.name


class PlaylistTrackPodcast(BaseModel):
    """Model for tracks/podcasts in playlists"""
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='items')
    track = models.ForeignKey('tracks.Track', on_delete=models.SET_NULL, null=True, blank=True, related_name='in_playlists')
    podcast_ep = models.ForeignKey('podcasts.PodcastEpisode', on_delete=models.SET_NULL, null=True, blank=True, related_name='in_playlists')
    
    order_index = models.IntegerField()
    added_by_user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='added_playlist_items')
    
    class Meta:
        ordering = ['order_index']
        verbose_name = 'Playlist Item'
        verbose_name_plural = 'Playlist Items'
        
    def __str__(self):
        item = self.track.title if self.track else self.podcast.title
        return f"{self.playlist} - {item} (#{self.order_index})"