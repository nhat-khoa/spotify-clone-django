from django.db import models
from apps.core.models import BaseModel  # Import BaseModel từ core


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
    podcast = models.ForeignKey('podcasts.Podcast', on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='podcasts')
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('podcast', 'category')
        verbose_name_plural = 'Podcast categories'
        
    def __str__(self):
        return f"{self.podcast} - {self.category}"