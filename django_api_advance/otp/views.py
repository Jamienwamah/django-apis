import json
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
from .models import OTP
from .serializers import OTPSerializer
from rent.serializers import UserSerializer

class RegisterUserView(APIView):
    def resend_otp(self, request):
        if request.method == 'POST':
            user_email = request.POST.get("otp_email")
            if get_user_model().objects.filter(email=user_email).exists():
                user = get_user_model().objects.get(email=user_email)
                otp = OTP.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
                subject = "Email Verified Successfully"
                message = f"Hi {user.username}, this one time otp code: {otp.otp_code}. is a confirmation that your email has been successfully verified. Please proceed to login "
                from_email = "rentspacedev@gmail.com"
                recipient = [user.email]
                
                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient,
                    fail_silently=False,
                )
                messages.success(request, "A new OTP has been sent to your email-address")
                return Response({"message": "A new OTP has been sent to your email-address"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "This email doesn't exist in the database"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
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