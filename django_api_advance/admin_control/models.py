from django.db import models

class AdminUser(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    # Add fields for AES and JWT keys
    aes_key = models.CharField(max_length=64, default='')
    jwt_secret_key = models.CharField(max_length=64, default='')  # Example: JWT secret key for signing tokens

    def is_active(self):
        return self.status == 'active'

    def __str__(self):
        return self.username
