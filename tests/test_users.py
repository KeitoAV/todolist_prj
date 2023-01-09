import pytest
from rest_framework import status

from core.models import User


@pytest.mark.django_db
def test_sign_up(client):
    data = {
        'username': 'test',
        'password': 'test_password',
        'password_repeat': 'test_password'
    }

    response = client.post(
        '/core/signup',
        data=data
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_get_user_profile(auth_client, user: User):
    expected_response = {
        'id': user.pk,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    response = auth_client.get('/core/profile')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_unauthorized_profile(client):
    response = client.get('/core/profile')

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_not_found(client):
    response = client.post('/cores/signup')

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_passwords_not_equal(client):
    data = {
        'username': 'test',
        'password': 'test_password',
        'password_repeat': 'test_password_1',
    }

    response = client.post(
        '/core/signup',
        data=data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
