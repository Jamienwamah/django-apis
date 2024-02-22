from django.db import models

class AccountDetails(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    # Add other fields as needed
