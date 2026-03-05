from django.db import models
from django.contrib.auth.models import AbstractUser
import re


class CustomUser(AbstractUser):
    """Extended user model with profile picture and phone number"""
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        default='profile_pictures/default_profile.jpg',
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return self.username
    
    def clean(self):
        """Validate phone number"""
        if self.phone_number:
            # Basic phone number validation (accepts formats like +1234567890 or 1234567890)
            if not re.match(r'^\+?1?\d{9,15}$', self.phone_number):
                raise ValueError("Phone number must be a valid format (9-15 digits, optionally starting with + or 1)")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
