import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Faker


User = get_user_model()
fake = Faker(locale="ru_RU")

USER_PASSWORD = "SecretPas123"


@pytest.fixture
def register_url():
    return reverse("users:register")


@pytest.fixture
def login_url():
    return reverse("users:login")


@pytest.fixture
def logout_url():
    return reverse("users:logout")


@pytest.fixture
def profile_url():
    return reverse("users:profile")


@pytest.fixture
def token_refresh_url():
    return reverse("users:token_refresh")


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def test_user_data():
    return {
        "email": fake.email(),
        "password": USER_PASSWORD,
        "password_confirm": USER_PASSWORD,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone": fake.phone_number(),
    }


@pytest.fixture
def test_user(test_user_data):
    test_user_data.pop("password_confirm")
    return User.objects.create_user(**test_user_data)
