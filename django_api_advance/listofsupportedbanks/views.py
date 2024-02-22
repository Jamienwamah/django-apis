import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SupportedBank
from .serializers import SupportedBankSerializer
from django.conf import settings

class SupportedBankListView(APIView):
    def get(self, request):
        try:
            # Define the URL of the Watu API endpoint for supported banks
            watu_supported_banks_url = 'https://api.watupay.com/v1/virtual-account/supported-banks/NG'  # Provide the actual URL

            # Define the Watu API key
            watu_api_key = settings.SECRET_KEY  # Replace with your actual Watu API key

            # Define headers with Watu API key
            headers = {
                'Authorization': f'Bearer {watu_api_key}',
                'Content-Type': 'application/json'
            }

            # Make a GET request to the Watu API endpoint
            response = requests.get(watu_supported_banks_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Print the response text for debugging
            print(response.text)

            # Parse the JSON response from the Watu API
            supported_banks_data = response.json()

            # Check if the response is a list
            if isinstance(supported_banks_data, list):
                # Iterate over the list of supported banks
                for bank_data in supported_banks_data:
                    # Check if the item is a dictionary
                    if isinstance(bank_data, dict):
                        bank_id = bank_data.get('id')  # Use get() method to avoid KeyError
                        bank_name = bank_data.get('name')  # Use get() method to avoid KeyError
                        local_reference = bank_data.get('local_reference')  # Use get() method to avoid KeyError

                        # Save or update the SupportedBank model instance
                        supported_bank, _ = SupportedBank.objects.update_or_create(
                            id=bank_id,
                            defaults={'name': bank_name, 'local_reference': local_reference}
                        )

                # Query the local database for supported banks
                supported_banks = SupportedBank.objects.all()
                serializer = SupportedBankSerializer(supported_banks, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': 'Unexpected response format'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.RequestException as e:
            # Handle request errors
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
