from django.contrib import admin
from .models import OTP

class OTPAdmin(admin.ModelAdmin):
    list_display = ('otp_code', 'otp_created_at', 'otp_expires_at', 'user')
    # Add other configurations as needed

admin.site.register(OTP, OTPAdmin)
