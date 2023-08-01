from rest_framework import serializers
from pages.models import Page, Tag, Post


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['__all__']
        extra_fields = {
            "tags": {'read_only': True},
            "owner": {'read_only': True},
            "followers": {'read_only': True},
            "image": {'read_only': True},
            "is_blocked": {'read_only': True},
            "follow_requests": {'read_only': True},
            "unblock_date": {'read_only': True},
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['__all__']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['__all__']
