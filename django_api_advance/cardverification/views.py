# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CardVerificationSerializer
from django.conf import settings
import requests

watu_api_key = settings.SECRET_KEY

@api_view(['POST'])
def verify_credit_card(request):
    serializer = CardVerificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        card_number = serializer.validated_data.get('card_number')
        exp_month = serializer.validated_data.get('exp_month')
        exp_year = serializer.validated_data.get('exp_year')
        cvc = serializer.validated_data.get('cvc')

        try:
            # Simulate verification process (replace with actual verification logic)
            if card_number and exp_month and exp_year and cvc:
                # Integration with Watu API (sample implementation)
                watu_api_url = ''
                watu_headers = {
                    'Authorization': f'Bearer {watu_api_key}',
                    'Content-Type': 'application/json'
                }
                watu_payload = {
                    'card_number': card_number,
                    'exp_month': exp_month,
                    'exp_year': exp_year,
                    'cvc': cvc,
                }

                watu_response = requests.post(watu_api_url, json=watu_payload, headers=watu_headers)

                if watu_response.status_code == 200:
                    return Response({'message': 'Credit card verified successfully'}, status=200)
                else:
                    return Response({'message': 'Failed to verify credit card with Watu API'}, status=500)
            else:
                return Response({'error': 'Invalid card details'}, status=400)
        except Exception as e:
            # Handle other errors
            return Response({'error': str(e)}, status=500)
    return Response(serializer.errors, status=400)
