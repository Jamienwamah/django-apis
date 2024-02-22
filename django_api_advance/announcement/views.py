import secrets

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from .models import Announcement
from .serializers import AnnouncementSerializer
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import os

class AESCipher:
    def __init__(self, key, iv=None):
        self.key = key.encode('utf-8')
        if iv:
            self.iv = iv
        else:
            self.iv = os.urandom(16)

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC, iv=self.iv)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        return iv, ct

    def decrypt(self, iv, data):
        iv = b64decode(iv)
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(b64decode(data)), AES.block_size)
        return pt.decode('utf-8')

class AnnouncementListView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def generate_aes_key(self):
        # Generate a random 32-byte (256-bit) key for AES encryption
        return secrets.token_bytes(32).hex()

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        # Generate JWT token
        token = AccessToken.for_user(request.user)

        # Generate AES key
        aes_key = self.generate_aes_key()

        aes_cipher = AESCipher(aes_key)
        encrypted_data = aes_cipher.encrypt(request.data)
        # Process the encrypted data as needed

        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        # The superuser's AES key can be stored in the database or retrieved from a secure location
        superuser_aes_key = "superuser_aes_key_here"
        aes_cipher = AESCipher(superuser_aes_key)
        encrypted_data = aes_cipher.encrypt(serializer.validated_data['data_to_encrypt'])
        serializer.save(encrypted_data=encrypted_data[1])
