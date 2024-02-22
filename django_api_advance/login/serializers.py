from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        models: get_user_model
        fields: '__all__'
    