# myapp/urls.py
from django.urls import path
from .views import fund_wallet

urlpatterns = [
    path('fund-wallet/', fund_wallet, name='fund_wallet'),
]
