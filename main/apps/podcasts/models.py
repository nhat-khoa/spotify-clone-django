from django.db import models
from apps.core.models import BaseModel  # Import BaseModel từ core
from apps.core.utils import generate_unique_filename

class Podcaster(BaseModel):
    """Model for podcast creators"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='podcaster_profile')
    bio = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.full_name or self.user.username


class Podcast(BaseModel):
    """Model for podcasts"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    podcaster = models.ForeignKey(Podcaster, on_delete=models.CASCADE, related_name='podcasts')
    public_web_url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    copyright_notice = models.CharField(max_length=255, blank=True)
    cover_art_image_url = models.ImageField(upload_to=generate_unique_filename)
    thumbnail_url = models.ImageField(upload_to=generate_unique_filename)
    description = models.JSONField(default=dict)
    rss_feed_url = models.URLField(blank=True)
    rss_feed_file = models.FileField(upload_to=generate_unique_filename, blank=True)
    licensor = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=50)
    explicit = models.BooleanField(default=False)
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    
    
    def __str__(self):
        return self.title


class PodcastRate(BaseModel):
    """Model for podcast ratings"""
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='podcast_ratings')
    rate = models.IntegerField()  # Assuming 1-5 scale
    
    class Meta:
        unique_together = ('podcast', 'user')
        
    def __str__(self):
        return f"{self.podcast} rated {self.rate} by {self.user}"


class PodcastEpisode(BaseModel):
    """Model for podcast episodes"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    TYPE_CHOICES = [
        ('full', 'Full Episode'),
        ('trailer', 'Trailer'),
        ('bonus', 'Bonus'),
    ]
    
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    audio_url = models.FileField(upload_to=generate_unique_filename,blank=True)
    transcript_url = models.FileField(upload_to=generate_unique_filename,blank=True)
    duration_seconds = models.IntegerField()
    season = models.IntegerField(null=True, blank=True)
    episode_number = models.IntegerField(null=True, blank=True)
    explicit = models.BooleanField(default=False)
    
    cover_art_image_url = models.ImageField(upload_to=generate_unique_filename, blank=True)
    is_featured = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='full')
    chapters = models.JSONField(default=dict, blank=True)
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    publish_date = models.DateTimeField(null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['season', 'episode_number']
        
    def __str__(self):
        return f"{self.podcast} - S{self.season}E{self.episode_number}: {self.title}"


class PodcastEpisodeComment(BaseModel):
    """Model for comments on podcast episodes"""
    episode = models.ForeignKey(PodcastEpisode, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='podcast_comments')
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    response_from_creator = models.TextField(blank=True)
    
    def __str__(self):
        return f"Comment on {self.episode} by {self.user}"
