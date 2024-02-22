from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from django.contrib.auth import logout

from .models import AccountUser
from .serializers import AccountUserSerializer
from rent.models import User  # Import the User model

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

class AccountUserView(generics.GenericAPIView):
    queryset = AccountUser.objects.all()
    serializer_class = AccountUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def generate_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT token
        token = self.generate_jwt_token(user)

        return Response(token, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(pk=request.user.id).first()  # Filter User model data based on the authenticated user
        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        account_user = AccountUser.objects.filter(user=user).first()  # Filter AccountUser model data based on the filtered User
        if not account_user:
            return Response({'error': 'Account user not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(account_user)
        
        # Check if the user is accessing their own account
        if account_user != request.user:
            return Response({'error': 'You do not have permission to access this account.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Encrypt user data
        key = get_random_bytes(16)
        aes_cipher = AESCipher(key)
        encrypted_data = aes_cipher.encrypt(str(serializer.data))
        
        return Response({'encrypted_data': encrypted_data}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        # Get the user object based on JWT token
        return self.request.user
