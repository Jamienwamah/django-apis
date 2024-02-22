from django.urls import path
from .views import SupportedBankListView

urlpatterns = [
    path('supported-banks/', SupportedBankListView.as_view(), name='supported_banks_list'),
]
