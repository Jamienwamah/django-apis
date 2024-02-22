from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import BvnDebitDetailsView

urlpatterns = [
    # Endpoint to refresh a user token
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Protected endpoint that requires user token authentication
    path('auth/bvn-debit-details/', BvnDebitDetailsView.as_view(), name='bvn-debit-details'),
]
