from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Notification
from .serializers import NotificationSerializer
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import jwt
from django.conf import settings

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        iv = cipher.iv
        ct = ct_bytes
        return iv, ct

    def decrypt(self, iv, data):
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(data), AES.block_size)
        return pt.decode('utf-8')

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]  # Only superusers can send notifications

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Generate JWT token
        token = jwt.encode({'user_id': request.user.id}, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

        # Generate AES key
        aes_key = get_random_bytes(16)
        aes_cipher = AESCipher(aes_key)

        # Encrypt notification content
        iv, encrypted_content = aes_cipher.encrypt(serializer.validated_data['content'])

        # Save encrypted content and token to database
        serializer.save(aes_key=aes_key, token=token)

        return Response({'token': token, 'iv': iv.hex(), 'encrypted_content': encrypted_content.hex()}, status=status.HTTP_201_CREATED)
