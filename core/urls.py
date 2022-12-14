from django.urls import path, include
from core import views
from core.views import SignUpView

urlpatterns = [

    path('', views.index),
    path('signup', SignUpView.as_view(), name='signup'),
]
