from rest_framework import serializers
from .models import OTP
from django.core.mail import send_mail
from django.conf import settings

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'

    def create(self, validated_data):
        # Generate OTP
        otp = self.generate_otp()

        # Save OTP in the database
        otp_instance = OTP.objects.create(**validated_data, otp=otp)

        # Send OTP via email
        subject = 'Your OTP for registration'
        message = f'Your OTP is: {otp}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [validated_data['user'].email]
        send_mail(subject, message, from_email, to_email)

        return otp_instance

    def generate_otp(self, length=6):
        # Generate a random OTP of specified length
        import random
        import string
        return ''.join(random.choices(string.digits, k=length))
