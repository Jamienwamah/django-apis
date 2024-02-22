# serializers.py
from rest_framework import serializers
from .models import PhoneVerification

class PhoneVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = '__all__'
