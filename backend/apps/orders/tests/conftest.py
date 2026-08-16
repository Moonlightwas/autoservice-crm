import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from faker import Faker

from apps.cars.models import Car


User = get_user_model()
fake = Faker(locale="ru_RU")

USER_PASSWORD = "SecretPas123"


@pytest.fixture
def order_url():
    return reverse("orders:order")


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def test_user_client():
    return User.objects.create_user(
        email=fake.email(),
        password=USER_PASSWORD,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone=fake.phone_number()
    )


def _test_car() -> Car:
    return Car.objects.create(
        client=test_user_client(),
        brand=fake.company(),
        model=fake.word(),
        year=fake.year(),
        vin=fake.vin(),
        plate_number=fake.text(10)
    )


@pytest.fixture
def test_order_data():
    return {
        "client": _test_user().id,
        "car": _test_car().id(),
        "description": fake.text(max_nb_chars=100)
    }
