import pytest
import re
from rest_framework import status
from django.contrib.auth import get_user_model

from .conftest import USER_PASSWORD


User = get_user_model()

pytestmark = pytest.mark.django_db


class TestRegisterView:
    def test_register_success(self, client, register_url, test_user_data):
        response = client.post(register_url, test_user_data)

        assert response.status_code == status.HTTP_201_CREATED

        user = User.objects.filter(email=test_user_data["email"]).first()
        assert user is not None

        assert user.email == test_user_data["email"]
        assert user.first_name == test_user_data["first_name"]
        assert user.last_name == test_user_data["last_name"]
        cleaned_phone = re.sub(r'[\s\-\(\)\.]', '',
                               test_user_data["phone"])
        if cleaned_phone[0] == "+":
            cleaned_phone = cleaned_phone[1:]
        assert user.phone == cleaned_phone

        assert user.role == "client"

        assert "password" not in response.data

    def test_register_duplicate_email(
            self, client, register_url, test_user, test_user_data
    ):
        assert User.objects.filter(email=test_user.email).exists()

        test_user_data["email"] = test_user.email
        response = client.post(register_url, test_user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize("field", ("email", "password", "password_confirm"))
    def test_missing_required_fields(
        self, client, register_url, test_user_data, field
    ):
        email = test_user_data.pop(field)

        response = client.post(register_url, test_user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert User.objects.filter(email=email).exists() is False


class TestLoginView:
    def test_login_success(self, client, login_url, test_user):
        response = client.post(login_url, {
            "email": test_user.email,
            "password": USER_PASSWORD}
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.data.get("access") is not None
        assert response.cookies.get("refresh_token") is not None

    def test_unregister_login(self, client, login_url, test_user_data):
        response = client.post(login_url, {
            "email": test_user_data["email"],
            "password": USER_PASSWORD}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert response.data.get("access") is None
        assert response.data.get("refresh") is None


class TestLogoutView:
    def test_logout_success(self, client, login_url, logout_url, test_user):
        client.force_authenticate(test_user)
        response = client.post(login_url, {
            "email": test_user.email,
            "password": USER_PASSWORD
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("access") is not None
        assert response.cookies.get("refresh_token") is not None

        response = client.post(logout_url)

        assert response.status_code == status.HTTP_200_OK


class TestTokenRefreshView:
    def test_refresh_success(
            self, client, login_url, token_refresh_url, test_user
    ):
        client.force_authenticate(test_user)
        response = client.post(login_url, {
            "email": test_user.email,
            "password": USER_PASSWORD
        })
        assert response.status_code == status.HTTP_200_OK

        response = client.post(token_refresh_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("access") is not None


class TestProfileView:
    def test_get_profile_success(self, client, profile_url, test_user):
        client.force_authenticate(test_user)

        response = client.get(profile_url)

        assert response.status_code == status.HTTP_200_OK

        assert response.data.get("email") == test_user.email
        assert response.data.get("first_name") == test_user.first_name
        assert response.data.get("last_name") == test_user.last_name
        assert response.data.get("phone") == test_user.phone
        assert response.data.get("role") == "client"

    @pytest.mark.parametrize(("field", "value", "expected"), (
        ("email", "new_email@test.com", "new_email@test.com"),
        ("first_name", "new_first_name", "new_first_name"),
        ("last_name", "new_last_name", "new_last_name"),
        ("phone", "+0 (123) 456 78-90", "01234567890")
    ))
    def test_patch_profile(
        self, client, profile_url, test_user, field, value, expected
    ):
        client.force_authenticate(test_user)

        response = client.patch(profile_url, data={field: value})

        user = User.objects.filter(email=test_user.email).first()

        assert response.status_code == status.HTTP_200_OK

        assert getattr(user, field) == expected
