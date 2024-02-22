# serializers.py
from rest_framework import serializers
from .models import BVNVerification

class BVNVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BVNVerification
        fields = '__all__'
