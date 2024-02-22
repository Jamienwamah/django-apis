from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PasswordReset
from .serializers import PasswordResetSerializer
import random
import string
from django.core.mail import send_mail
from django.conf import settings

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Generate a random OTP
            otp = ''.join(random.choices(string.digits, k=6))

            # Save the OTP in the database
            password_reset, created = PasswordReset.objects.get_or_create(email=email)
            password_reset.otp = otp
            password_reset.save()

            # Send OTP via email
            send_mail(
                'Reset Password OTP',
                f'Your OTP for resetting the password is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return Response({"message": "Reset password OTP sent to your email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
