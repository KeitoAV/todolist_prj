from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
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


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        )
        if not user:
            raise AuthenticationFailed()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data["old_password"]):
            raise serializers.ValidationError({"old_password": "Неправильный пароль"})

        validate_password(validated_data["new_password"])
        instance.set_password(validated_data["new_password"])
        instance.save()

        return instance
