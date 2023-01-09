import pytest
from rest_framework import status

from goals.models import (
    Board,
    BoardParticipant,
    Goal
)
from goals.serializers import GoalSerializer


URL = '/goals/goal/list'


# goal_create
@pytest.mark.django_db
def test_success(auth_client, goal: Goal, goal_category: GoalSerializer, board_participant):
    data = {
        'title': goal.title,
        'category': goal_category.pk
    }

    response = auth_client.post(
        '/goals/goal/create',
        data=data
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == goal.title


@pytest.mark.django_db
def test_no_goal(auth_client, goal: Goal, board_participant: BoardParticipant):
    data = {
        'title': goal.title,
    }

    response = auth_client.post(
        '/goals/goal/create',
        data=data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# goal_list
@pytest.mark.django_db
def test_no_goals(auth_client):
    response = auth_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.django_db
def test_not_participant(auth_client, user, board):
    assert BoardParticipant.objects.filter(user_id=user.pk).count() == 0
    assert Board.objects.count() == 1

    response = auth_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.django_db
@pytest.mark.parametrize('board_participant__role',
                         [BoardParticipant.Role.owner, BoardParticipant.Role.writer, BoardParticipant.Role.reader],
                         ids=['owner', 'writer', 'reader'])
def test_board_participant(auth_client, goal: Goal, board_participant: BoardParticipant,
                           board_participant__role: BoardParticipant):
    response = auth_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == goal.id
    assert data[0]['category'] == goal.category.pk
    assert data[0]['title'] == goal.title


# goal_retrieve
@pytest.mark.django_db
def test_retrieve_goal(auth_client, goal: Goal, board_participant: BoardParticipant):
    response = auth_client.get(f'/goals/goal/{goal.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == GoalSerializer(goal).data


@pytest.mark.django_db
def test_not_found(client):
    response = client.get('/goals/goal')

    assert response.status_code == status.HTTP_404_NOT_FOUND
