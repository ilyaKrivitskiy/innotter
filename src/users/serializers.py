from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'title', 'is_blocked', 'is_superuser', 'is_staff']


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True}
        }
