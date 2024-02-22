from django.urls import path
from .views import ForgotPasswordView

urlpatterns = [
    path('reset-password/', ForgotPasswordView.as_view(), name='reset-password'),
]
