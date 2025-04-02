from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
import uuid
from django.utils.translation import gettext_lazy as _
from apps.core.utils import generate_unique_filename

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email là bắt buộc')
        email = self.normalize_email(email)
        
        # Set username = email
        extra_fields.setdefault('username', email)  
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    gender = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    age = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    subscription_type = models.CharField(max_length=50, blank=True)
    
    avatar_url = models.ImageField(upload_to=generate_unique_filename,blank=True)
    thumbnail_url = models.ImageField(upload_to=generate_unique_filename,blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    avatar_google_url = models.CharField(max_length=900, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email