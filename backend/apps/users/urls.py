from django.urls import path, include

from .auth_views import (RegisterView, LoginView,
                         LogoutView, CustomRefreshTokenView)
from .users_views import ProfileView, UsersViewSet


app_name = "users"

auth_urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "token/refresh/",
        CustomRefreshTokenView.as_view(),
        name="token_refresh"
    ),
]

users_urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("", UsersViewSet.as_view({"get": "list"}), name="users"),
    path("<int:pk>/", UsersViewSet.as_view(
        {"get": "retrieve"}), name="user-detail"
    ),
]

urlpatterns = [
    path("auth/", include(auth_urlpatterns)),
    path("users/", include(users_urlpatterns)),
]
