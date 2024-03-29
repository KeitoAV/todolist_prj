from django.urls import path

from goals.views import (
    BoardCreateView,
    BoardListView,
    BoardView,
    CommentCreateView,
    CommentsListView,
    CommentView,
    GoalCategoryCreateView,
    GoalCategoryListView,
    GoalCategoryView,
    GoalCreateView,
    GoalListView,
    GoalView
)


urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view(), name='category_create'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='category_list'),
    path('goal_category/<pk>', GoalCategoryView.as_view(), name='category'),

    path('goal/create', GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', GoalListView.as_view(), name='goal_list'),
    path('goal/<pk>', GoalView.as_view(), name='goal'),

    path('goal_comment/create', CommentCreateView.as_view(), name='comment_create'),
    path('goal_comment/list', CommentsListView.as_view(), name='comments_list'),
    path('goal_comment/<pk>', CommentView.as_view(), name='comment'),

    path('board/create', BoardCreateView.as_view(), name='board_create'),
    path('board/list', BoardListView.as_view(), name='boards_list'),
    path('board/<pk>', BoardView.as_view(), name='board'),
]
