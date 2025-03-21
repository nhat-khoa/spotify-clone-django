from django.db import models
import uuid
# Create your models here.

class BaseModel(models.Model):
    """Base model that uses UUID as primary key."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True