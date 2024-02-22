# loans/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests
from .models import CustomerLoan
from .serializers import CustomerLoanSerializer

@api_view(['POST'])
def create_loan(request):
    serializer = CustomerLoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Integrate with Watu API to create the loan
        watu_loan_api_url = 'https://api.watupay.com/v1/payment/initiate'
        watu_api_key = 'settings.SECRET_KEY'

        headers = {
            'Authorization': f'Bearer {watu_api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'customer_id': serializer.validated_data['id'],
            # Add other loan data as needed
        }

        watu_response = requests.post(watu_loan_api_url, json=payload, headers=headers)

        if watu_response.status_code == 200:
            return Response(serializer.data, status=201)
        else:
            # Rollback the customer creation in your database if Watu API call fails
            CustomerLoan.objects.filter(id=serializer.data['id']).delete()
            return Response({'message': 'Failed to create loan in Watu API'}, status=watu_response.status_code)
    return Response(serializer.errors, status=400)
