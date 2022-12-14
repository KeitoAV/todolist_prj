from django.http import HttpResponse
from rest_framework.generics import CreateAPIView

from core.models import User
from core.serializers import SignUpSerializer


def index(request):
    return HttpResponse("Python developer course. Graduation project. Task planner.")


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
