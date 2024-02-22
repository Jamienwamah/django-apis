# accounts/models.py
from django.db import models

class Forgot(models.Model):
    email = models.EmailField(unique=True)
    reset_token = models.CharField(max_length=100, null=True, blank=True)
