from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import BoardPermissions, GoalCategoryPermission, GoalPermission, CommentPermission
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, CommentCreateSerializer, CommentSerializer, BoardCreateSerializer, BoardListSerializer, \
    BoardSerializer


# category
class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermission]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ('board',)
    ordering_fields = ('title', 'created',)
    ordering = ('title', 'created',)
    search_fields = ('title',)

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False,
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermission]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False,
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.goals.update(status=Goal.Status.archived)
            for goal in instance.goals.all():
                goal.status = goal.Status.archived
                goal.save()
        return instance


# goal
class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalListView(ListAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermission]
    pagination_class = LimitOffsetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ('title', 'created', 'id',)
    ordering = ('title',)
    search_fields = ('title',)

    def get_queryset(self):
        return self.model.objects.filter(category__board__participants__user=self.request.user
                                         ).exclude(status=self.model.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermission]

    def get_queryset(self):
        return self.model.objects.filter(category__board__participants__user=self.request.user
                                         ).exclude(status=self.model.Status.archived)

    def perform_destroy(self, instance):
        instance.status = self.model.Status.archived
        instance.save()
        return instance


# comment
class CommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentsListView(ListAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]
    pagination_class = LimitOffsetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ('goal',)
    ordering = ('-created',)

    def get_queryset(self):
        return self.model.objects.filter(goal__category__board__participants__user=self.request.user)


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]

    def get_queryset(self):
        return self.model.objects.filter(goal__category__board__participants__user=self.request.user)


# board
class BoardCreateView(CreateAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class BoardListView(ListAPIView):
    model = Board
    serializer_class = BoardListSerializer
    permission_classes = [BoardPermissions]
    pagination_class = LimitOffsetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    ordering = ('title',)
    search_fields = ('title',)

    def get_queryset(self):
        return self.model.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return self.model.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance
