# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BVNVerificationViewSet

router = DefaultRouter()
router.register(r'bvn-verification', BVNVerificationViewSet, basename='bvn-verification')

urlpatterns = [
    path('', include(router.urls)),
]
