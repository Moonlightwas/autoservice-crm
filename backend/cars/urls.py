from django.urls import path

from .views import CarViewSet


app_name = "cars"

urlpatterns = [
    path("", CarViewSet.as_view(
        {"get": "list", "post": "create"}),
        name="car"
    ),
    path("<int:pk>", CarViewSet.as_view(
        {"get": "retrieve"}),
        name="car-detail"
    ),
]
