from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VirtualAccount
from django.conf import settings
from .serializers import VirtualAccountSerializer
import requests

@api_view(['POST'])
def create_virtual_account(request):
    serializer = VirtualAccountSerializer(data=request.data)
    if serializer.is_valid():
        # Save the validated data to create a new VirtualAccount instance
        virtual_account = serializer.save()

        try:
            # Integrate with Watu's API to get the list of supported banks
            watu_supported_banks_url = '#'
            code_api_key = settings.SECRET_KEY

            headers = {
                'Authorization': f'Bearer {code_api_key}',
                'Content-Type': 'application/json'
            }

            watu_response = requests.get(watu_supported_banks_url, headers=headers)
            watu_response.raise_for_status()  # Raise an exception for HTTP errors

            supported_banks = watu_response.json()

            # Retrieve the selected bank ID from the serializer's validated data
            bank_id = serializer.validated_data['bank']

            # Check if the selected bank ID is in the list of supported banks
            if bank_id not in supported_banks:
                # Delete the created VirtualAccount instance if the selected bank is not supported
                virtual_account.delete()
                return Response({'message': 'Selected bank is not supported'}, status=status.HTTP_400_BAD_REQUEST)

            # Get the bank ID from the list of supported banks
            bank_id = supported_banks[bank_id]

            # Integrate with Watu's API to create the virtual account using the validated data and bank ID
            watu_create_virtual_account_url = '#'

            watu_payload = {
                'account_name': virtual_account.account_name,
                'business_wallet_id': virtual_account.business_wallet_id,
                'bank': bank_id,
                'customer_email': virtual_account.customer_email,
                # Include other relevant fields from the VirtualAccount model
            }

            watu_response = requests.post(watu_create_virtual_account_url, json=watu_payload, headers=headers)
            watu_response.raise_for_status()  # Raise an exception for HTTP errors

            # If integration with Watu's API is successful, return a success message
            return Response({'message': 'Virtual account created successfully'}, status=status.HTTP_201_CREATED)

        except requests.RequestException as e:
            # Handle request errors
            virtual_account.delete()  # Delete the created VirtualAccount instance
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
