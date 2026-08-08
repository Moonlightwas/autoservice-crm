from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("apps.users.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/cars/", include("apps.cars.urls")),
]
