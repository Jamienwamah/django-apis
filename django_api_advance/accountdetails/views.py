from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import AccountDetails
from django.conf import settings
from .serializers import UserAccountSerializer
import requests

@api_view(['GET'])
def get_user_account_details(request):
    # Replace placeholders with actual values
    watu_api_url = ''  # Replace with the actual Watu API URL for account details
    access_token = 'settings.CLIENT_KEY'  # Replace with your Watu access token
    
    # Set headers with access token
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Make API call to Watu to retrieve account details
    try:
        response = requests.get(watu_api_url, headers=headers)

        # Process the response
        if response.status_code == 200:
            account_details = response.json()
            serializer = UserAccountSerializer(data=account_details)
            
            if serializer.is_valid():
                # Save account details to database (optional)
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response({'message': 'Failed to fetch account details from Watu'}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response({'message': f'Error connecting to Watu API: {e}'}, status=500)
