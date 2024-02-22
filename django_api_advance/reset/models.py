from django.contrib.auth.models import User
from django.db import models

class PasswordReset(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    old_password = models.CharField(max_length=128, default='')  # Assuming the old password will be hashed
    new_password = models.CharField(max_length=128, default='')  # Assuming the new password will be hashed
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Password reset for {self.user.username}"
