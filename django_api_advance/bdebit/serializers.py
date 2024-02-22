# serializers.py
from rest_framework import serializers
from .models import BvnDebitUser

class BvnDebitDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BvnDebitUser
        fields = '__all__'

