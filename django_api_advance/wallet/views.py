# myapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from .models import Wallet
import requests

@api_view(['POST'])
def fund_wallet(request):
    user = request.user
    amount = request.data.get('amount')

    # Integrate with Watu Wallet API
    watu_wallet_api_url = '#'
    watu_wallet_api_key = 'settings.SECRET_KEY'

    headers = {
        'Authorization': f'Bearer {watu_wallet_api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'user_id': user.id,
        'amount': amount
    }

    watu_response = requests.post(watu_wallet_api_url, json=payload, headers=headers)

    if watu_response.status_code == 200:
        # Update the user's wallet balance in your database
        wallet, created = Wallet.objects.get_or_create(user=user)
        wallet.balance += float(amount)
        wallet.save()

        return Response({'message': 'Wallet funded successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Failed to fund wallet'}, status=watu_response.status_code)
