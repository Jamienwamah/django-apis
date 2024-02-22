# serializers.py
from rest_framework import serializers
from .models import AdminUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'username', 'status']
