from django.db import models
from apps.core.models import BaseModel  # Import BaseModel từ core
from apps.core.utils import generate_unique_filename

class Folder(BaseModel):
    """Model for folders to organize playlists"""
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='folders')
    
    def __str__(self):
        return self.name


class Playlist(BaseModel):
    """Model for playlists"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_playlists')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    avatar_url = models.ImageField(upload_to=generate_unique_filename, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    likes_count = models.IntegerField(default=0)
    collaborators = models.JSONField(default=dict, blank=True)
    items = models.JSONField(default=dict, blank=True)  # List of track IDs or podcast episode IDs
    """ 
    items = [
        {
            "uid": "unique_id_1",
            "item_type": "track",  # or "podcast_episode"
            "item_id": "item_id_1",
            "item_name": "Track Name",
            "owner_id": "artist_id_1", # artist_id or podcaster_id
            "owner_name": "Artist Name or Podcaster Name", 
            "album_or_podcast": "Album or podcast Name",
            "album_or_podcast_id": "Album or podcast ID",
            "item_image": "https://example.com/image.jpg",
            "item_duration_ms": 180000,  # in milliseconds,
            "created_at": "2023-10-01T12:00:00Z",
        }
    ]
    """
    
    def __str__(self):
        return self.name

class UserFollowedArtist(BaseModel):
    """Model for users following artists"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='followed_artists')
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE, related_name='followers')
    
    
    class Meta:
        unique_together = ('user', 'artist')
        
    def __str__(self):
        return f"{self.user} follows {self.artist}"


class UserFollowedPodcast(BaseModel):
    """Model for users following podcasts"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='followed_podcasts')
    podcast = models.ForeignKey('podcasts.Podcast', on_delete=models.CASCADE, related_name='followers')
    
    
    class Meta:
        unique_together = ('user', 'podcast')
        
    def __str__(self):
        return f"{self.user} follows {self.podcast}"


class UserFollowedPlaylist(BaseModel):
    """Model for users following playlists"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='followed_playlists')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='followers')
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name='playlists')
    
    class Meta:
        unique_together = ('user', 'playlist')
        
    def __str__(self):
        return f"{self.user} follows {self.playlist}"
    
    
class UserSavedTrack(BaseModel):
    """Model for tracks saved by users"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='saved_tracks')
    track = models.ForeignKey('tracks.Track', on_delete=models.CASCADE, related_name='saved_by')
    
    
    class Meta:
        unique_together = ('user', 'track')
        
    def __str__(self):
        return f"{self.user} saved {self.track}"


class UserSavedAlbum(BaseModel):
    """Model for albums saved by users"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='saved_albums')
    album = models.ForeignKey('albums.Album', on_delete=models.CASCADE, related_name='saved_by')
    
    
    class Meta:
        unique_together = ('user', 'album')
        
    def __str__(self):
        return f"{self.user} saved {self.album}"
    
    
class UserSavedEpisode(BaseModel):
    """Model for podcast episodes saved by users"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='saved_episodes')
    episode = models.ForeignKey('podcasts.PodcastEpisode', on_delete=models.CASCADE, related_name='saved_by')   
    
    
    class Meta:
        unique_together = ('user', 'episode')
        
    def __str__(self):
        return f"{self.user} saved {self.episode}"