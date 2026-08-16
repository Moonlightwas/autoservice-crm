from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .serializers import (
    CarSerializer,
    CarListSerializer,
    CarDetailSerializer,
    CarCreateSerializer
)
from .models import Car
from apps.core.permissions import IsCarOwner


class CarViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsCarOwner]

    def get_serializer_class(self):
        if self.action == "list":
            return CarListSerializer
        elif self.action == "create":
            return CarCreateSerializer
        elif self.action == "retrieve":
            return CarDetailSerializer
        return CarSerializer

    def get_queryset(self):
        queryset = Car.objects.all().select_related("owner")
        user = self.request.user

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(owner__email__icontains=search) |
                Q(owner__first_name__icontains=search) |
                Q(owner__last_name__icontains=search) |
                Q(brand__icontains=search) |
                Q(model__icontains=search) |
                Q(year__icontains=search) |
                Q(vin__icontains=search) |
                Q(plate_number__icontains=search)
            )

        if user.is_superuser or user.is_staff or user.role in ("manager", "admin"):
            return queryset

        if user.role == "mechanic":
            return queryset.filter(orders__mechanic=user)

        return queryset.filter(owner=user)

    def perform_create(self, serializer):
        user = self.request.user

        if (user.is_superuser or user.is_staff or user.role in ("manager", "admin")):
            serializer.save()
        else:
            serializer.save(owner=user)
