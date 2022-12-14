from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.models import User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    @staticmethod
    def validate_password(data):
        validate_password(data)
        return data

    def create(self, validated_data):
        password = validated_data.get('password')
        password_repeat = validated_data.pop('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError('Введенные пароли не совпадают, повторите попытку')

        validated_data['password'] = make_password(password)

        return super().create(validated_data)
