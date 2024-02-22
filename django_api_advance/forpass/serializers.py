# serializers.py
from rest_framework import serializers
from .models import Forgot

class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forgot
        fields = ['email', 'reset_token']
