from pytest_factoryboy import register

from tests.factories import (
    BoardFactory,
    BoardParticipantFactory,
    CategoryFactory,
    GoalFactory,
    UserFactory
)


pytest_plugins = 'tests.fixtures'

register(UserFactory)
register(BoardFactory)
register(BoardParticipantFactory)
register(CategoryFactory)
register(GoalFactory)
