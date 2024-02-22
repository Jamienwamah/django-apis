from django.urls import path, include
from rest_framework import routers
from kyc.views import KYCVerificationViewSet

router = routers.DefaultRouter()
router.register(r'kyc', KYCVerificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
