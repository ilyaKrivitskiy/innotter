from rest_framework import serializers
from pages.models import Page, Tag, Post


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'
        extra_fields = {
            "tags": {'required': False},
            "owner": {'read_only': True},
            "followers": {'read_only': True},
            "image": {'read_only': True, 'required': False},
            "is_blocked": {'read_only': True},
            "follow_requests": {'read_only': True, 'required': False},
            "unblock_date": {'read_only': True},
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
