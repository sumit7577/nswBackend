from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from app.models import *


class UserDetailSerialzer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password","phone","image"]


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=200)
    password = serializers.CharField(required=True, max_length=128)