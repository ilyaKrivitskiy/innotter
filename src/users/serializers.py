from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'role', 'title', 'is_blocked',
                  'is_superuser', 'is_staff']

        extra_kwargs = {
            'email': {'read_only': True},
            'is_blocked': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
        }


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True}
        }
