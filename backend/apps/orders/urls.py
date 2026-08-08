from django.urls import path

from .views import OrderViewSet


app_name = "orders"

urlpatterns = [
    path("", OrderViewSet.as_view(
        {"get": "list", "post": "create"}),
        name="order"
    ),
    path("<int:pk>/", OrderViewSet.as_view({
        "get": "retrieve",
        "patch": "partial_update",
        "delete": "destroy"
    }), name="order-detail"),


    path("<int:pk>/force-status/", OrderViewSet.as_view({
        "patch": "force_status"
    }), name="order-force-status"),

    path("<int:pk>/confirm/", OrderViewSet.as_view({
        "post": "confirm"
    }), name="order-confirm"),

    path("<int:pk>/start_work/", OrderViewSet.as_view({
        "post": "start_work"
    }), name="order-start-work"),

    path("<int:pk>/ready/", OrderViewSet.as_view({
        "post": "ready"
    }), name="order-ready"),

    path("<int:pk>/confirm_pay/", OrderViewSet.as_view({
        "post": "confirm_pay"
    }), name="order-confirm-pay"),

    path("<int:pk>/complete/", OrderViewSet.as_view({
        "post": "complete"
    }), name="order-complete"),

    path("<int:pk>/cancel/", OrderViewSet.as_view({
        "post": "cancel"
    }), name="order-cancel"),
]
