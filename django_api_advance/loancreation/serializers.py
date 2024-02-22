# loans/serializers.py
from rest_framework import serializers
from .models import CustomerLoan

class CustomerLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLoan
        fields = '__all__'
