from rest_framework import serializers
from .models import VirtualAccount
from listofsupportedbanks.models import SupportedBank  # Import the SupportedBank model

class VirtualAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualAccount
        fields = '__all__'

    def validate_bank(self, value):
        # Check if the provided bank exists in the list of supported banks
        supported_banks = SupportedBank.objects.values_list('name', flat=True)
        if value not in supported_banks:
            raise serializers.ValidationError("Selected bank is not supported.")
        return value