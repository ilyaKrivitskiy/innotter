from django.db import models


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    is_private = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        'pages.Tag',
        related_name='pages',
        blank=True
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='pages',
        blank=True
    )
    followers = models.ManyToManyField(
        'users.User',
        related_name='follows',
        default=[]
    )
    image = models.URLField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(
        'users.User',
        related_name='requests',
        default=[]
    )
    unblock_date = models.DateTimeField(null=True, blank=True)
    objects = models.Manager()


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    objects = models.Manager()


class Post(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey(
        'pages.Post',
        on_delete=models.SET_NULL,
        null=True,
        related_name='replies'
    )
    likes = models.ManyToManyField(
        'users.User',
        related_name='likes',
        default=[]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
