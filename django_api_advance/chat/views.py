from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from .models import FAQ
from .serializers import FAQSerializer
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from django.conf import settings

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

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Decrypt any confidential information before returning
        aes_cipher = AESCipher(settings.SECRET_KEY)
        decrypted_content = aes_cipher.decrypt(serializer.data['encrypted_content_iv'], serializer.data['encrypted_content'])
        serializer.data['content'] = decrypted_content

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        raise PermissionDenied("You do not have permission to create FAQ content.")

    def update(self, request, *args, **kwargs):
        raise PermissionDenied("You do not have permission to update FAQ content.")

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("You do not have permission to delete FAQ content.")
