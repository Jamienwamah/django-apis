from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import logout
from django.conf import settings
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

from .models import BvnDebitUser
from .serializers import BvnDebitDetailsSerializer

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

class BvnDebitDetailsView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = BvnDebitUser.objects.all()
    serializer_class = BvnDebitDetailsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Check if user is superuser
        if not request.user.is_superuser:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        # Generate a random 16-byte key
        key = get_random_bytes(16)
        aes_cipher = AESCipher(key)
        iv, ct = aes_cipher.encrypt(serializer.data)

        return Response({'iv': iv, 'encrypted_data': ct}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Check if user is superuser
        if not request.user.is_superuser:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the key from the request
        key = request.data.get('key')
        iv, ct = serializer.data.get('iv'), serializer.data.get('encrypted_data')

        aes_cipher = AESCipher(key)
        decrypted_data = aes_cipher.decrypt(iv, ct)

        return Response({'decrypted_data': decrypted_data}, status=status.HTTP_200_OK)
