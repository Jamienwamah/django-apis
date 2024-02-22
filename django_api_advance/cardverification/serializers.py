# serializers.py
from rest_framework import serializers
from .models import CardVerification

class CardVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardVerification
        fields = '__all__'
