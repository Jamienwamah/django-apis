# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import Loan, Debit
from .serializers import LoanSerializer, DebitSerializer
import requests

@api_view(['POST'])
def create_loan(request):
    serializer = LoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Integration with Watu API to record loan debit
        watu_api_url = '#'
        watu_api_key = 'settings.SECRET_KEY'  # Replace with your actual Watu API key

        payload = {
            'loan_id': serializer.data['id'],
            'amount': serializer.data['amount']
        }

        headers = {
            'Authorization': f'Bearer {watu_api_key}',
            'Content-Type': 'application/json'
        }

        watu_response = requests.post(watu_api_url, json=payload, headers=headers)

        if watu_response.status_code == 200:
            return Response(serializer.data, status=201)
        else:
            # Rollback the loan creation if Watu API call fails
            Loan.objects.filter(id=serializer.data['id']).delete()
            return Response({'message': 'Failed to record loan debit with Watu API'}, status=500)
    return Response(serializer.errors, status=400)
