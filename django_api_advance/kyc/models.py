from django.db import models
from django.contrib.auth.models import User

class KYCVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    # Add other fields as needed
