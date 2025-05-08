from django.db import models
from apps.core.models import BaseModel  # Import BaseModel từ core
from apps.core.utils import generate_unique_filename

class Artist(BaseModel):
    """Model for artists"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='artist_profile')
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True)
    avatar_url =  models.ImageField(upload_to=generate_unique_filename, null=True, blank=True)
    thumbnail_url = models.ImageField(upload_to=generate_unique_filename, null=True, blank=True)
    popularity = models.IntegerField(default=0)
    country = models.CharField(max_length=100, blank=True)
    more_info = models.JSONField(default=dict, blank=True)
    
    
    def __str__(self):
        return self.name


class ArtistImageGallery(BaseModel):
    """Model for artist image gallery"""
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='gallery_images')
    image_url = models.ImageField(upload_to=generate_unique_filename)
    title = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    file_size = models.IntegerField(null=True, blank=True)
    display_order = models.IntegerField(default=0)
    
    
    class Meta:
        ordering = ['display_order']
        verbose_name_plural = 'Artist image galleries'
        
    def __str__(self):
        return f"{self.artist} - {self.title}"
    
    

class ArtistPick(BaseModel):
    """Model for artist picks"""
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='picks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active_from = models.DateTimeField()
    active_until = models.DateTimeField(null=True, blank=True)  # NULL means no expiration
    is_active = models.BooleanField(default=True)
    custom_message = models.TextField(blank=True)
    image_url = models.ImageField(upload_to=generate_unique_filename)
    
    # Content reference - only one of these should be used
    track = models.ForeignKey('tracks.Track', on_delete=models.SET_NULL, null=True, blank=True, related_name='artist_picks')
    album = models.ForeignKey('albums.Album', on_delete=models.SET_NULL, null=True, blank=True, related_name='artist_picks')
    playlist = models.ForeignKey('interactions.Playlist', on_delete=models.SET_NULL, null=True, blank=True, related_name='artist_picks')
    podcast = models.ForeignKey('podcasts.Podcast', on_delete=models.SET_NULL, null=True, blank=True, related_name='artist_picks')
    episode = models.ForeignKey('podcasts.PodcastEpisode', on_delete=models.SET_NULL, null=True, blank=True, related_name='artist_picks')
    external_url = models.URLField(blank=True)

    
    def __str__(self):
        return f"{self.artist} - {self.title}"