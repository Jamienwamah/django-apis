from rest_framework import serializers
from .models import AdminHistory

class AdminHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminHistory
        fields = ['id', 'action', 'email', 'user_id', 'login_time', 'logout_time', 'role', 'session_id']
