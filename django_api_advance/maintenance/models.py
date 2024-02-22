from django.db import models

class Maintenance(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    description = models.TextField(default='')
    start_date = models.DateField(default='')
    end_date = models.DateField(default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # Additional fields for encrypted data
    encrypted_field = models.TextField(default='')  # Example field for storing encrypted data
    encrypted_field_iv = models.CharField(max_length=24, default='')  # Initialization vector for AES encryption
