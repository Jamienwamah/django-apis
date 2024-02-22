from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import SpaceRentProfile
from .serializers import SpaceRentProfileSerializer
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

class SpaceRentProfileCreateView(generics.CreateAPIView):
    serializer_class = SpaceRentProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Encrypt data before saving
        rent_amount = serializer.validated_data.get('rent_amount')
        due_date = serializer.validated_data.get('due_date')
        savings_interval = serializer.validated_data.get('savings_interval')
        created_at = serializer.validated_data.get('created_at')
        space_rent_id = self.request.user

        key = self.request.user.profile.encryption_key  # Assuming user profile has encryption key
        cipher = AES.new(key.encode(), AES.MODE_CBC)
        data = f"{rent_amount},{due_date},{savings_interval},{created_at},{created_by.id},{space_rent_id}"
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        encrypted_data = b64encode(ct_bytes).decode()

        serializer.save(encrypted_data=encrypted_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SpaceRentProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = SpaceRentProfile.objects.all()
    serializer_class = SpaceRentProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Decrypt data before returning
        key = self.request.user.profile.encryption_key  # Assuming user profile has encryption key
        iv = b64decode(instance.encrypted_data)[:AES.block_size]
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(b64decode(instance.encrypted_data)), AES.block_size)
        decrypted_data = pt.decode()
        rent_amount, due_date, savings_interval, created_at, created_by_id, space_rent_id = decrypted_data.split(',')
        
        data = {
            'rent_amount': float(rent_amount),
            'due_date': due_date,
            'savings_interval': savings_interval,
            'created_at': created_at,
            'created_by': int(created_by_id),
            'space_rent_id': int(space_rent_id)
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Decrypt data before updating
        key = self.request.user.profile.encryption_key  # Assuming user profile has encryption key
        iv = b64decode(instance.encrypted_data)[:AES.block_size]
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(b64decode(instance.encrypted_data)), AES.block_size)
        decrypted_data = pt.decode()
        rent_amount, due_date, savings_interval, created_at, created_by_id, space_rent_id = decrypted_data.split(',')
        
        data = {
            'rent_amount': float(rent_amount),
            'due_date': due_date,
            'savings_interval': savings_interval,
            'created_at': created_at,
            'created_by': int(created_by_id),
            'space_rent_id': int(space_rent_id)
        }

        serializer.save(data)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
