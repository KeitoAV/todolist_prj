# Generated by Django 4.0.1 on 2023-01-07 11:49

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import (
    migrations,
    models
)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_chat_id', models.IntegerField(verbose_name='id чата')),
                ('tg_user_id', models.IntegerField(verbose_name='id пользователя Телеграмм')),
                ('tg_username', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Пользователь Телеграмм')),
                ('verification_code', models.CharField(max_length=10, unique=True, verbose_name='Kод подтверждения')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь из приложения')),
            ],
            options={
                'verbose_name': 'Telegram пользователь',
                'verbose_name_plural': 'Telegram пользователи',
            },
        ),
    ]
