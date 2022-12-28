from django.contrib import admin
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


# category
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')


# goal
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')


# comment
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'goal', 'created', 'updated',)
    search_fields = ('text', 'user',)


# board
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'role',)
    search_fields = ('board', 'user', 'role',)


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
