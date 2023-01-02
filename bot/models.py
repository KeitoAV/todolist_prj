from django.db import models
from core.models import User


class TgUser(models.Model):
    telegram_chat_id = models.IntegerField(verbose_name='id чата')
    telegram_user_id = models.IntegerField(verbose_name='id пользователя Телеграмм')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Пользователь API')
