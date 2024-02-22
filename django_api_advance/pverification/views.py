from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import PhoneVerification
from .serializers import PhoneVerificationSerializer
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import jwt
from django.conf import settings

class PhoneVerificationViewSet(viewsets.ModelViewSet):
    queryset = PhoneVerification.objects.all()
    serializer_class = PhoneVerificationSerializer

    @staticmethod
    def generate_jwt_token(phone_number):
        payload = {'phone_number': phone_number}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_jwt_token(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload['phone_number']
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return None
        except jwt.InvalidTokenError:
            # Handle invalid token
            return None

    @staticmethod
    def encrypt_verification_code(verification_code):
        aes_cipher = AES.new(settings.SECRET_KEY[:32], AES.MODE_CBC)
        encrypted_code = aes_cipher.encrypt(pad(verification_code.encode(), AES.block_size))
        return b64encode(encrypted_code).decode()

    @staticmethod
    def decrypt_verification_code(encrypted_code):
        aes_cipher = AES.new(settings.SECRET_KEY[:32], AES.MODE_CBC)
        decrypted_code = unpad(aes_cipher.decrypt(b64decode(encrypted_code)), AES.block_size)
        return decrypted_code.decode()

    @action(detail=False, methods=['post'])
    def verify_phone_number(self, request):
        phone_number = request.data.get('phone_number')
        encrypted_verification_code = request.data.get('encrypted_verification_code')

        # Verify JWT token
        token = request.headers.get('Authorization').split()[1]
        decoded_phone_number = self.verify_jwt_token(token)
        if decoded_phone_number != phone_number:
            return Response({'message': 'Invalid phone number or token'}, status=status.HTTP_401_UNAUTHORIZED)

        # Decrypt verification code
        verification_code = self.decrypt_verification_code(encrypted_verification_code)

        try:
            phone_verification = PhoneVerification.objects.get(phone_number=phone_number, verification_code=verification_code)
        except PhoneVerification.DoesNotExist:
            return Response({'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

        phone_verification.is_verified = True
        phone_verification.save()

        return Response({'message': 'Phone number verified successfully'})
