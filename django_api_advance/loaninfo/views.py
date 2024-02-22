# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LoanSerializer
from django.conf import settings
import requests

@api_view(['GET'])
def get_loans(request):
    # Integration with Watu API to retrieve loan information
    watu_api_url = 'https://api.watupay.com/v1/payment/initiate'
    watu_api_key = 'settings.SECRET_KEY'  # Replace with your actual Watu API key

    headers = {
        'Authorization': f'Bearer {watu_api_key}',
    }

    watu_response = requests.get(watu_api_url, headers=headers)

    if watu_response.status_code == 200:
        loans_data = watu_response.json()
        serializer = LoanSerializer(loans_data, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response({'message': 'Failed to retrieve loan information from Watu API'}, status=500)
