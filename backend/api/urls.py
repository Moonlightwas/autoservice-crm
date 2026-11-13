from django.urls import path, include


urlpatterns = [
    path('', include('users.urls')),
    path('orders/', include('orders.urls')),
    path('cars/', include('cars.urls')),
]
