from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import AccountUserView

urlpatterns = [
    path('auth/account/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain JWT token
    path('auth/account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT token
    path('auth/account/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verify JWT token
    path('auth/profile/', AccountUserView.as_view(), name='profile'),  # User registration view
]
