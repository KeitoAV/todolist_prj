from django.contrib import admin
from django.urls import (
    include,
    path
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('goals/', include('goals.urls')),
    path('bot/', include('bot.urls')),

]
