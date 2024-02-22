# urls.py
from django.urls import path
from .views import create_loan

urlpatterns = [
    path('create-loan/', create_loan, name='create_loan'),
]
