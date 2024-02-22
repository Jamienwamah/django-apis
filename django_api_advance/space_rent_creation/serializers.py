from rest_framework import serializers
from .models import SpaceRentProfile

class SpaceRentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceRentProfile
        fields = '__all__'

    def create(self, validated_data):
        # Assuming 'created_by' is a field in your model
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
