from rest_framework import permissions

from apps.orders.models import Order


class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ("manager", "admin")


class IsOrderStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Is manager or admin.
        if user.is_superuser or user.role in ("manager", "admin"):
            return True

        if user.role == "mechanic":
            # Mechanic is allowed to start_work and ready order.
            if view.action in ("start_work", "ready"):
                return obj.mechanic.filter(id=user.id).exists()
            # Mechanics can get only his own order.
            if view.action in ("retrieve"):
                return obj.mechanic.filter(id=user.id).exists()

        if user.role == "client":
            # Client can get, partitial update and cancel only his own order.
            if view.action in ("retrieve", "partial_update", "cancel"):
                return obj.client == user

        return False


class IsCarOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Is manager or admin.
        if user.is_superuser or user.role in ("manager", "admin"):
            return True

        if user.role == "mechanic":
            return Order.objects.filter(
                car=obj,
                mechanic=user
            ).exists()

        return obj.owner == user
