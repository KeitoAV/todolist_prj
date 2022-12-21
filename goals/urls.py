from django.urls import path
from goals.views import GoalCategoryCreateView, GoalCategoryView, GoalCategoryListView, GoalCreateView, GoalListView, \
    GoalView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view(), name='category_create'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='category_list'),
    path('goal_category/<pk>', GoalCategoryView.as_view(), name='category'),

    path('goal/create', GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', GoalListView.as_view(), name='goal_list'),
    path('goal/<pk>', GoalView.as_view(), name='goal'),
]
