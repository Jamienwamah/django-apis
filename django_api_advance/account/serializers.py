# serializers.py
from rest_framework import serializers
from .models import AccountUser

class AccountUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = '__all__'
