from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
    email = models.EmailField(null=True, unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)
