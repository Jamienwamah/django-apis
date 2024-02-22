from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceViewSet

# Create a router and register the MaintenanceViewSet with it
router = DefaultRouter()
router.register(r'maintenance', MaintenanceViewSet)

urlpatterns = [
    # Add the router URLs to the urlpatterns
    path('', include(router.urls)),
]
