import pytest
from rest_framework import status

from core.models import User
from goals.models import (
    Board,
    BoardParticipant,
    GoalCategory
)
from goals.serializers import GoalCategorySerializer


URL = '/goals/goal_category/list'


# goal_category_create
@pytest.mark.django_db
def test_success(auth_client, goal_category: GoalCategory, board_participant: Board):
    data = {
        'title': goal_category.title,
        'board': board_participant.board.pk,
        'user': board_participant.user_id
    }

    response = auth_client.post(
        '/goals/goal_category/create',
        data=data
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == goal_category.title


@pytest.mark.django_db
def test_no_board(auth_client, goal_category: GoalCategory, board_participant: Board):
    data = {
        'title': goal_category.title,
        'user': board_participant.user_id
    }

    response = auth_client.post(
        '/goals/goal_category/create',
        data=data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# goal_category_list
@pytest.mark.django_db
def test_no_categories(auth_client):
    response = auth_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.django_db
def test_not_participant(auth_client, user: User, board: Board):
    assert BoardParticipant.objects.filter(user_id=user.pk).count() == 0
    assert Board.objects.count() == 1

    response = auth_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.django_db
@pytest.mark.parametrize('board_participant__role',
                         [BoardParticipant.Role.owner, BoardParticipant.Role.writer, BoardParticipant.Role.reader],
                         ids=['owner', 'writer', 'reader'])
def test_board_participant(auth_client, goal_category: GoalCategory, board_participant: BoardParticipant,
                           board_participant__role: BoardParticipant):
    response = auth_client.get(URL)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == goal_category.id
    assert data[0]['is_deleted'] is False
    assert data[0]['title'] == goal_category.title


# goal_category_retrieve
@pytest.mark.django_db
def test_retrieve_category(auth_client, goal_category: GoalCategory, board_participant: BoardParticipant):
    response = auth_client.get(f'/goals/goal_category/{goal_category.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == GoalCategorySerializer(goal_category).data


@pytest.mark.django_db
def test_not_found(client):
    response = client.get('/goals/goal_category')

    assert response.status_code == status.HTTP_404_NOT_FOUND
