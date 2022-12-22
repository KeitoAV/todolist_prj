from django.contrib import admin
from goals.models import GoalCategory, Goal, GoalComment


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
    list_display = ('text', 'user', 'goal', 'created', 'updated')
    search_fields = ('text', 'user')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
