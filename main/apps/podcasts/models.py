from django.db import models
from apps.core.models import BaseModel  # Import BaseModel từ core
from apps.core.utils import generate_unique_filename

class Podcaster(BaseModel):
    """Model for podcast creators"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='podcaster_profile')
    name = models.CharField(max_length=255, default='', null=True, blank=True)
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
    title = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    copyright_notice = models.CharField(max_length=255, blank=True,null=True)
    cover_art_image_url = models.ImageField(upload_to=generate_unique_filename, blank=True, null=True)
    thumbnail_url = models.ImageField(upload_to=generate_unique_filename, blank=True, null=True)
    description = models.JSONField(default=dict, blank=True, null=True)
    rss_feed_url = models.URLField(blank=True,null=True)
    rss_feed_file = models.FileField(upload_to=generate_unique_filename, blank=True,null=True)
    licensor = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=50, blank=True)
    explicit = models.BooleanField(default=False)
    rate = models.JSONField(default=dict, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    
    
    def __str__(self):
        return self.title


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
    description = models.TextField(blank=True, null=True)
    audio_url = models.FileField(upload_to=generate_unique_filename,blank=True, null=True) 
    transcript_url = models.FileField(upload_to=generate_unique_filename,blank=True, null=True)
    duration_ms = models.IntegerField( null=True, blank=True)
    season = models.IntegerField(null=True, blank=True)
    episode_number = models.IntegerField(null=True, blank=True)
    explicit = models.BooleanField(default=False)
    
    cover_art_image_url = models.ImageField(upload_to=generate_unique_filename, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='full')
    chapters = models.JSONField(default=dict, blank=True)
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    publish_date = models.DateTimeField(null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    
    comments = models.JSONField(default=dict, blank=True, null=True)
    
    class Meta:
        ordering = ['season', 'episode_number']
        
    def __str__(self):
        return f"{self.podcast} - S{self.season}E{self.episode_number}: {self.title}"



class Category(BaseModel):
    """Model for categories"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name


class PodcastCategory(BaseModel):
    """Model for podcast categories"""
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='podcasts')
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('podcast', 'category')
        verbose_name_plural = 'Podcast categories'
        
    def __str__(self):
        return f"{self.podcast} - {self.category}"