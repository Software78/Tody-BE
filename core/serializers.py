from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class SignupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
            validated_data["password"] = make_password(validated_data.get("password"))
            return super(SignupSerializer, self).create(validated_data)
    class Meta:
            model = User
            fields = ['username','password']

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
            model = User
            fields = ['username','password']