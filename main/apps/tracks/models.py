from django.db import models
from apps.core.models import BaseModel  # Import BaseModel từ core
from apps.core.utils import generate_unique_filename

class Track(BaseModel):
    """Model for tracks"""
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE, related_name='created_tracks')
    album = models.ForeignKey('albums.Album', on_delete=models.CASCADE, related_name='tracks', null=True, blank=True)
    
    title = models.CharField(max_length=255)
    duration_ms = models.IntegerField()  # in seconds
    popularity = models.IntegerField(default=0)
    audio_file_path = models.FileField(upload_to=generate_unique_filename,blank=True)
    isrc_code = models.CharField(max_length=50, blank=True)  # International Standard Recording Code
    explicit = models.BooleanField(default=False)
    language = models.CharField(max_length=50, blank=True)
    release_date = models.DateField(null=True, blank=True)
    
    plain_lyrics = models.TextField(blank=True)
    synced_lyrics = models.FileField(upload_to=generate_unique_filename,blank=True)
    record_label = models.CharField(max_length=255, blank=True)
    is_instrumental = models.BooleanField(default=False)
    
    source = models.CharField(max_length=255,blank=True)
    
    def __str__(self):
        return self.title


class TrackArtist(BaseModel):
    """Model for track artists (for collaborations)"""
    ROLE_CHOICES = [
        
        ('primary', 'Primary Artist'),
        ('featured', 'Featured Artist'),
        ('remixer', 'Remixer'),
        ('composer', 'Composer'),
        
        # produced
        ('producer', 'Producer'),
        ('co-producer', 'Co-Producer'),
        ('executive', 'Executive Producer'),
        ('engineer', 'Engineer'),
        ('mixer', 'Mixer'),
        
        # written  
        ('writer', 'Writer Artist, Both Music and Lyrics'),
        ('writer_music', 'Music'),
        ('writer_lyrics', 'Lyrics'),

        # perform
        ('performer', 'Performer Artist'),
        ('lead', 'Lead Vocalist'),
        ('backing', 'Backing Vocalist'),
        ('instrumentalist', 'Instrumentalist'),

        ('other', 'Other'),
    ]
    
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE, related_name='track_credits')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='credited_artists')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='primary')
    
    class Meta:
        unique_together = ('artist', 'track', 'role')
        
    def __str__(self):
        return f"{self.artist} - {self.track} ({self.role})"