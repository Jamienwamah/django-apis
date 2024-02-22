from rest_framework import viewsets
from .models import KYCVerification
from .serializers import KYCVerificationSerializer

class KYCVerificationViewSet(viewsets.ModelViewSet):
    queryset = KYCVerification.objects.all()
    serializer_class = KYCVerificationSerializer
