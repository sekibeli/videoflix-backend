from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, default='')
    adress = models.CharField(max_length=150, default='')
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
