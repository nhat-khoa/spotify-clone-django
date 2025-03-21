from django.db import models
from apps.core.models import BaseModel  # Import BaseModel từ core

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
    playlist = models.ForeignKey('playlists.Playlist', on_delete=models.CASCADE, related_name='followers')
    folder = models.ForeignKey('playlists.Folder', on_delete=models.SET_NULL, null=True, blank=True, related_name='playlists')

    
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