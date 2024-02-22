from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Maintenance
from .serializers import MaintenanceSerializer
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from django.contrib.auth.models import User

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

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Encrypt sensitive information before storing
            aes_cipher = AESCipher(settings.SECRET_KEY)
            encrypted_description_iv, encrypted_description = aes_cipher.encrypt(serializer.data['description'])
            serializer.validated_data['description'] = encrypted_description
            serializer.validated_data['description_iv'] = encrypted_description_iv
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def decrypt_description(self, request, pk=None):
        instance = self.get_object()
        aes_cipher = AESCipher(settings.SECRET_KEY)
        decrypted_description = aes_cipher.decrypt(instance.description_iv, instance.description)
        return Response({'decrypted_description': decrypted_description})
