from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Car


User = get_user_model()


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class CarListSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = "__all__"

    def get_owner(self, obj):
        if obj.owner:
            return {
                "email": obj.owner.email,
            }
        return None


class CarDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = "__all__"

    def get_owner(self, obj):
        if obj.owner:
            return {
                "id": obj.owner.id,
                "email": obj.owner.email,
                "first_name": obj.owner.first_name,
                "last_name": obj.owner.last_name,
                "phone": obj.owner.phone,
                "role": obj.owner.role
            }
        return None

    def get_orders(self, obj):
        orders = obj.orders.all().order_by('-created_at')

        return [
            {
                "id": order.id,
                "description": order.description,
                "status": order.status,
                "mechanic": [
                    m.get_full_name() or m.email for m in order.mechanic.all()
                ],
                "created_at": order.created_at
            }
            for order in orders
        ]


class CarCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="client"),
        error_messages={"does_not_exist": "Invalid car's owner"}
    )

    class Meta:
        model = Car
        fields = "__all__"

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user

        if not (user.is_superuser or user.is_staff or user.role in ("manager", "admin")):
            owner = attrs.get("owner")
            if owner and owner != user:
                raise serializers.ValidationError(
                    {"owner": "Invalid car's owner"}
                )

        return attrs
