from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
    OrderForceStatusSerializer
)
from .models import Order
from apps.core.permissions import IsOrderStaff


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrderStaff]

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        elif self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderDetailSerializer
        elif self.action == "force_status":
            return OrderForceStatusSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if self.action == "list":
            queryset = (Order.objects.all()
                        .select_related("car")
                        .only("id", "status", "description", "status",
                              "created_at", "car__brand", "car__model"))
        else:
            queryset = (Order.objects.all()
                        .select_related("client", "car")
                        .prefetch_related("mechanic"))

        if user.role in ("mechanic"):
            return queryset.filter(mechanic=user)

        status = self.request.query_params.get("status")
        if status and status.lower() != "all":
            queryset = queryset.filter(status=status)

        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(client=user_id)

        if user.is_superuser or user.is_staff or user.role in ("manager", "admin"):
            return queryset

        return queryset.filter(client=user)

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_superuser or user.is_staff or user.role in ("manager", "admin"):
            serializer.save(source=Order.Source.MANAGER)
        else:
            serializer.save(
                client=user,
                source=Order.Source.ONLINE
            )

    def perform_destroy(self, instance):
        user = self.request.user

        if user.is_superuser or user.is_staff or user.role in ("manager", "admin"):
            instance.delete()
        raise PermissionDenied

    def _change_status(self, method_name):
        order = self.get_object()
        changed = getattr(order, method_name)()

        if changed:
            return Response(
                {
                    "message": "Order status changed successfully",
                    "current_status": order.status
                },
                status.HTTP_200_OK
            )
        return Response(
            {"detail": f"Can't change order status from '{order.status}' to '{method_name}'"},
            status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["post"])
    def force_status(self, request, pk=None):
        order = self.get_object()
        user = request.user

        if not (user.is_superuser or user.is_staff or user.role in ("manager", "admin")):
            return Response(
                {"detail": "User doesn't has permission"},
                status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_status = request.data.get("status")
        if order.set_status_force(new_status):
            return Response(
                {
                    "message": "Order status changed successfully",
                    "current_status": order.status
                },
                status.HTTP_200_OK)
        return Response(
            {"detail": f"Can't change order status from '{order.status}' to '{new_status}'"},
            status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        return self._change_status("confirm")

    @action(detail=True, methods=["post"])
    def start_work(self, request, pk=None):
        return self._change_status("start_work")

    @action(detail=True, methods=["post"])
    def ready(self, request, pk=None):
        return self._change_status("ready")

    @action(detail=True, methods=["post"])
    def confirm_pay(self, request, pk=None):
        return self._change_status("confirm_pay")

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        return self._change_status("complete")

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        return self._change_status("cancel")
