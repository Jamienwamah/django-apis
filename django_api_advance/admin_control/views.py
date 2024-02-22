from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

from django.conf import settings
from .models import AdminUser
from .serializers import CustomUserSerializer

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        return iv, ct

    def decrypt(self, iv, data):
        cipher = AES.new(self.key, AES.MODE_CBC, b64decode(iv))
        pt = unpad(cipher.decrypt(b64decode(data)), AES.block_size)
        return pt.decode('utf-8')

class CustomTokenAuthentication(TokenAuthentication):
    def not_authenticated(self, request):
        raise AuthenticationFailed(
            'You must log in.', code=status.HTTP_401_UNAUTHORIZED)

    def authenticate_credentials(self, key):
        try:
            user, token = super().authenticate_credentials(key)
        except Exception as e:
            raise AuthenticationFailed(
                {'Error': 'User needs to log in'}, code=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            logout(user)  # Automatically log out inactive users
            raise AuthenticationFailed(
                {'error': 'Please log in'}, code=status.HTTP_401_UNAUTHORIZED)

        return user, token

    def authentication_failed(self, request, message=None, code=None):
        raise AuthenticationFailed(
            {'error': 'Please log in'}, code=status.HTTP_401_UNAUTHORIZED)

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class UserStatusView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request, username):
        try:
            user = AdminUser.objects.get(username=username)
            serializer = CustomUserSerializer(user)
            aes_cipher = AESCipher(settings.SECRET_KEY)
            encrypted_data = aes_cipher.encrypt(serializer.data)
            return Response({'status': encrypted_data}, status=status.HTTP_200_OK)
        except AdminUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Generate JWT token
        token = AccessToken.for_user(request.user)

        # Encrypt data using AES
        aes_cipher = AESCipher(settings.SECRET_KEY)
        encrypted_data = aes_cipher.encrypt(str(token))

        return Response({'token': encrypted_data}, status=status.HTTP_200_OK)
