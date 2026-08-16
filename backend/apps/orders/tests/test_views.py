import pytest
from rest_framework import status


pytestmark = pytest.mark.django_db


class TestOrderViewSet:
    def test_create_order_success(self, client, test_user_client, order_url):
        client.force_authenticate(test_user_client)

        response = client.post(order_url)

        print(response.data)

        assert response.status_code == status.HTTP_201_CREATED
