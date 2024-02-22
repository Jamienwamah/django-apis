# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('landlord/confirm/', views.confirm_payment, name='confirm_payment'),
]
