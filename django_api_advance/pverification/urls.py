# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhoneVerificationViewSet

router = DefaultRouter()
router.register(r'phone-verification', PhoneVerificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
