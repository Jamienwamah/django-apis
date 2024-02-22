# urls.py
from django.urls import path
from .views import verify_credit_card

urlpatterns = [
    path('verify-credit-card/', verify_credit_card, name='verify_credit_card'),
]
