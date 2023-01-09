import pytest
from rest_framework.test import APIClient

from core.models import User


@pytest.fixture
@pytest.mark.django_db
def auth_client(client, user: User) -> APIClient:
    client.force_login(user)
    return client
