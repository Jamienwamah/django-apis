# serializers.py - Create a serializer to handle loan data retrieved from Watu API
from rest_framework import serializers

class LoanSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields as needed
