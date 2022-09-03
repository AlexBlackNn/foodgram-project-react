from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings

from .models import User, Tag


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей со статусом admin."""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user

    class Meta:
        model = User
        fields = (
            'username', 'password', 'email', 'first_name', 'last_name', 'role'
        )


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей со статусом admin."""

    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
             'password', 'email'
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для tags."""

    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')

