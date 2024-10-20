"""This module defines serializers for the User model.

Classes:
    UserSerializer: A serializer for the User model.
"""

from typing import ClassVar

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """A serializer for the User model.

    Meta:
        model (User): The model to be serialized.
        fields (list): The fields to be included in the serialization.
        read_only_fields (list): The fields to be marked as read-only.
        extra_kwargs (dict): Extra keyword arguments for the fields.
    """

    class Meta:
        model = User
        fields: ClassVar = [
            "id",
            "email",
            "telephone",
            "image",
            "telegram_user_id",
            "is_verified",
            "is_active",
            "date_modified",
        ]
        read_only_fields: ClassVar = [
            "is_verified",
            "is_active",
            "date_modified",
        ]
        extra_kwargs: ClassVar = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """Create a new user instance.

        Args:
            validated_data (dict): The validated data for creating the user.

        Returns:
            User: The created user instance.
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing user instance.

        Args:
            instance (User): The existing user instance.
            validated_data (dict): The validated data for updating the user.

        Returns:
            User: The updated user instance.
        """
        instance.email = validated_data.get("email", instance.email)
        instance.telephone = validated_data.get(
            "telephone", instance.telephone
        )
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance
