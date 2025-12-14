from .models import CustomUser
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from django.contrib.auth import authenticate


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name", "password"]
        write_only_fields = ["password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class ProfileSerializer(ModelSerializer):
    date_joined_formatted = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "date_joined_formatted",
        ]
        read_only_fields = ["id", "email", "date_joined"]

    def get_date_joined_formatted(self, obj):
        # Format the date as you want it displayed
        if obj.date_joined:
            # Format: "November 30, 2025"
            return obj.date_joined.strftime("%d %B, %Y")
        return None


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Incorrect Credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data["user"] = user
        return data

    def to_representation(self, instance):
        # This defines what data gets returned in the response
        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            # Add other fields as needed
        }


class ChangePasswordSerializer(Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def valida_old_password(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError("Old password is incorrect")
        return attrs
