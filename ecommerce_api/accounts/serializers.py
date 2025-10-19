
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta: fields = ("username","email","password"); model = User
    def create(self, data):
        user = User(username=data["username"], email=data.get("email"))
        user.set_password(data["password"]); user.save(); return user

class UserSerializer(serializers.ModelSerializer):
    class Meta: model = User; fields = ("id","username","email","is_staff")
    read_only_fields = ("id","is_staff")
