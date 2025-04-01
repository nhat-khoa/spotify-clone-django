from django.db import models
from apps.core.models import BaseModel  # Import BaseModel từ core
from apps.core.utils import generate_unique_filename

class Album(BaseModel):
    """Model for albums"""
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    avatar_url =  models.ImageField(upload_to=generate_unique_filename, null=True, blank=True)
    cover_art_url =  models.ImageField(upload_to=generate_unique_filename, null=True, blank=True)
    album_type = models.CharField(max_length=50, blank=True)  # single, EP, album, etc.
    label = models.CharField(max_length=255, blank=True)
    copyright = models.CharField(max_length=255, blank=True)
    is_public = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.title
    
    
class AlbumArtist(BaseModel):
    """Model for album artists (for collaborations)"""
    ROLE_CHOICES = [
        ('primary', 'Primary Artist'),
        ('performer', 'Performer Artist'),
        ('writer', 'Writer Artist'),
        ('featured', 'Featured Artist'),
        ('producer', 'Producer'),
        ('composer', 'Composer'),
        ('other', 'Other'),
    ]
    
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE, related_name='album_credits')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='contributing_artists')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='primary')
    
    
    class Meta:
        unique_together = ('artist', 'album', 'role')
        
    def __str__(self):
        return f"{self.artist} - {self.album} ({self.role})"