from rest_framework import serializers
from .models import KYCVerification

class KYCVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCVerification
        fields = '__all__'
