from rest_framework import serializers
from .models import SupportedBank

class SupportedBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportedBank
        fields = ['id', 'name', 'local_reference']
