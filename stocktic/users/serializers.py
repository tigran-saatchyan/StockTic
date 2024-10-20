from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "telephone",
            "image",
            "telegram_user_id",
            "is_verified",
            "is_active",
            "date_modified",
        ]
        read_only_fields = ["is_verified", "is_active", "date_modified"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.telephone = validated_data.get("telephone", instance.telephone)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance
