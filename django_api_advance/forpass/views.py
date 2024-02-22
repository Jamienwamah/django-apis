# views.py
import json
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from otp.models import OTP
from .models import Forgot
from .serializers import ForgotPasswordSerializer
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
import random
import string

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            

            # Check if a "forgot" request with the email already exists
            forgot_request, created = Forgot.objects.get_or_create(email=email)

            if not created:
                # If a request already exists, update it with a new reset token
                reset_token = ''.join(random.choices(string.digits, k=4))
                forgot_request.reset_token = reset_token
                forgot_request.save()
            else:
                # If a new request is created, generate a reset token and save it
                reset_token = ''.join(random.choices(string.digits, k=4))
                forgot_request.reset_token = reset_token
                forgot_request.save()

            # Send email with reset token (replace with your email sending logic)
            send_mail(
                'Reset Password',
                f'Your reset password token is: {reset_token}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return Response({"message": "Reset otp email sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """def post(self, request, *args, **kwargs):
        # Your password reset logic here
        return Response("Password reset request received", status=status.HTTP_200_OK)
        """

    
logger = logging.getLogger(__name__)

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        try:
            # Parse the request body as JSON
            request_data = json.loads(request.body.decode('utf-8'))
            
            # Retrieve the submitted OTP from the parsed JSON data
            submitted_otp = request_data.get('otp')
            
            logger.info("Submitted OTP: %s", submitted_otp)  # Log the submitted OTP
        except json.JSONDecodeError:
            logger.error("Invalid JSON data")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        if submitted_otp:
            try:
                # Retrieve the OTP object from the database
                stored_otp_obj = OTP.objects.get(otp_code=submitted_otp)
            except OTP.DoesNotExist:
                logger.error("OTP not found")
                return JsonResponse({'error': 'OTP not found'}, status=404)
            
            # OTP found, delete it from the database
            stored_otp_obj.delete()
            return JsonResponse({'message': 'OTP verification successful'})
        else:
            logger.error("OTP not provided")
            return JsonResponse({'error': 'OTP not provided'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)