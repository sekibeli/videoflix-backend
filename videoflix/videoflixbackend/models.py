from datetime import date
from django.db import models
from django.conf import settings


# Create your models here.

class Category(models.TextChoices):
        allgemein = 'allgemein'
        kids = 'kids'
        funny = 'funny'
        noidea = 'noidea'
        
class Video(models.Model):
    
    created_at = models.DateField(default=date.today)
    created_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.allgemein)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    likes = models.ManyToManyField('user.CustomUser', related_name='likers', blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', null=True, blank=True)
    view_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

