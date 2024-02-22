# serializers.py
from rest_framework import serializers
from .models import Loan, Debit

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class DebitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debit
        fields = '__all__'
