from rest_framework import serializers

from .models import Order
from apps.cars.models import Car
from apps.cars.serializers import CarSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderListSerializer(serializers.ModelSerializer):
    car = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "status", "description", "status", "created_at", "car"]

    def get_car(self, obj):
        if obj.car:
            return {
                "brand": obj.car.brand,
                "model": obj.car.model
            }
        return None


class OrderDetailSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "created_at", "updated_at", "started_at", "completed_at"
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(),
        required=True,
        error_messages={"does_not_exist": "Invalid car"}
    )

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "status",
            "source",
            "total_price",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            "source": {"required": False}
        }

    def validate(self, attrs):
        request = self.context.get("request")

        user = request.user

        if user.is_superuser or user.is_staff or user.role in ("manager", "admin"):
            return attrs

        client = attrs.get("client", user)
        car = attrs.get("car")

        if car and car.owner != client:
            raise serializers.ValidationError(
                {"car": "Invalid car field"}
            )

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.car:
            representation["car"] = CarSerializer(instance.car).data

        return representation


class OrderForceStatusSerializer(serializers.Serializer):
    status = serializers.CharField()
