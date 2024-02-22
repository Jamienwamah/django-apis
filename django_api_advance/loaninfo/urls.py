# urls.py
from django.urls import path
from .views import get_loans

urlpatterns = [
    path('get-loans/', get_loans, name='get_loans'),
]
