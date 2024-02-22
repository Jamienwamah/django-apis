from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def confirm_payment(request):
    if request.method == 'POST':
        # Extract payment details from request data
        payment_id = request.data.get('payment_id')
        amount = request.data.get('amount')
        # Verify payment details (e.g., using a payment gateway API)
        # Update payment status in the database
        # Return success response
        return Response({'message': 'Payment confirmed successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

