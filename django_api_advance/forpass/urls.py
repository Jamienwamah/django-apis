from django.urls import path
from .views import ForgotPasswordView
from . import views

urlpatterns = [
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-forgotpassword-otp/', views.verify_otp, name='verify_otp'),
]