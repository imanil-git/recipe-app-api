"""
Serializers for Healthcare APIs.
"""
from rest_framework import serializers
from core.models import Specialization


class SpecializationSerializer(serializers.ModelSerializer):
    """Serializers for Specializations objects."""

    class Meta:
        model = Specialization
        fields = ('id', 'user', 'name', 'slug', 'specialty', 'description', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')