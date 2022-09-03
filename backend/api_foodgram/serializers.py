from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для tags."""

    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')

