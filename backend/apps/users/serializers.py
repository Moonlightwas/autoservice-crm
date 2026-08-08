from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User
from .validators import validate_phone_number


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "role"]

    def validate_phone(self, value):
        return validate_phone_number(value)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "role",
        ]


class UserListSerializer(serializers.ModelSerializer):
    orders_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "role",
            "orders_count",
        ]

    def validate_phone(self, value):
        return validate_phone_number(value)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(required=True)
    first_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True)
    phone = serializers.CharField(
        max_length=20, required=False, allow_blank=True)

    def validate_phone(self, value):
        return validate_phone_number(value)

    def validate(self, data):
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "passwords don't match"}
            )
        data.pop("password_confirm")

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone"]
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "phone": {"required": False},
        }

    def validate_phone(self, value):
        return validate_phone_number(value)
