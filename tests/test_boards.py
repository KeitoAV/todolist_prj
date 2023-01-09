import pytest
from rest_framework import status

from core.models import User
from goals.models import (
    Board,
    BoardParticipant
)
# board_create
from goals.serializers import BoardSerializer


@pytest.mark.django_db
def test_success(auth_client: User, board: Board):
    data = {
        'title': board.title,
    }

    response = auth_client.post(
        '/goals/board/create',
        data=data
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == board.title


@pytest.mark.django_db
def test_unauthorized(client: User, board: Board):
    data = {
        'title': board.title,
    }

    response = client.post(
        '/goals/board/create',
        data=data
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# board_list
@pytest.mark.django_db
class TestBoardListView:

    def test_no_boards_in_db(self, auth_client: User):
        response = auth_client.get('/goals/board/list')
        assert response.status_code == 200
        assert response.json() == []

    def test_not_participant(self, user: User, client: User, board: Board):
        assert BoardParticipant.objects.filter(user_id=user.id).count() == 0
        assert Board.objects.count() == 1

        client.force_login(user)
        response = client.get('/goals/board/list')
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.parametrize('board_participant__role', [
        BoardParticipant.Role.owner,
        BoardParticipant.Role.writer,
        BoardParticipant.Role.reader,
    ], ids=['owner', 'writer', 'reader'])
    def test_board_participant(self, auth_client: User, board_participant: BoardParticipant,
                               board_participant__role: BoardParticipant):
        response = auth_client.get('/goals/board/list')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['id'] == board_participant.board.id
        assert data[0]['is_deleted'] is False
        assert data[0]['title'] == board_participant.board.title

    @pytest.mark.parametrize('board__is_deleted, boards_count', [
        (True, 0),
        (False, 1)
    ], ids=['deleted', 'not deleted'])
    def test_is_deleted(self, auth_client: User, board: Board, board_participant: BoardParticipant,
                        boards_count: Board, board__is_deleted):
        response = auth_client.get('/goals/board/list')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == boards_count


# goal_retrieve
@pytest.mark.django_db
def test_retrieve_board(auth_client: User, board: Board, board_participant: BoardParticipant):
    response = auth_client.get(f'/goals/board/{board.pk}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == BoardSerializer(board).data
