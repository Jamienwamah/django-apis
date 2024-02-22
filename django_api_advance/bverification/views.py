from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import BVNVerification
from .serializers import BVNVerificationSerializer
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
import os

class BVNVerificationViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user  # Authenticated user
        bvn = request.data.get('bvn')
        key = self.generate_aes_key()  # Generate AES key dynamically
        
        encrypted_bvn = self.encrypt_bvn(bvn, key)

        is_verified = self.verify_bvn(bvn)

        if is_verified:
            bvn_obj = BVNVerification.objects.create(user=user, bvn=encrypted_bvn, is_verified=True)
            serializer = BVNVerificationSerializer(bvn_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "BVN verification failed"}, status=status.HTTP_400_BAD_REQUEST)

    def encrypt_bvn(self, bvn, key):
        cipher = AES.new(key.encode(), AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(bvn.encode(), AES.block_size))
        encrypted_bvn = b64encode(ct_bytes).decode()
        return encrypted_bvn

    def verify_bvn(self, bvn):
        return True  # Placeholder for actual BVN verification logic

    @staticmethod
    def generate_aes_key():
        # Generate a random 16-byte AES key
        key = os.urandom(16)
        return key.hex()
