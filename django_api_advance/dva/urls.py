# myapp/urls.py
from django.urls import path
from .views import create_virtual_account

urlpatterns = [
    path('create-virtual-account/', create_virtual_account, name='create_virtual_account'),
]
