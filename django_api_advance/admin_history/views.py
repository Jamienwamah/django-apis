from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

from django.conf import settings  # Import Django settings

from .models import AdminHistory
from .serializers import AdminHistorySerializer

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

class AdminHistoryView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = AdminHistory.objects.all()
    serializer_class = AdminHistorySerializer

    def perform_create(self, serializer):
        aes_cipher = AESCipher(settings.SECRET_KEY)
        encrypted_data = aes_cipher.encrypt(self.request.data['data_to_encrypt'])
        serializer.save(encrypted_data=encrypted_data[1])

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        
        token = AccessToken.for_user(request.user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to perform this action.")
        
        serializer.save()
