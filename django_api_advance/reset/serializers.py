from rest_framework import serializers
from .models import PasswordReset

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = '__all__'
