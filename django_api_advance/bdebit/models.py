from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid

TRANSACTION_TYPES = [
    ('debit', 'Debit'),
    ('credit', 'Credit'),
]

class BvnDebitUser(AbstractUser):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    charge_date = models.DateField()
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    
    groups = models.ManyToManyField(
        Group, related_name='bdebit_groups', blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='bdebit_user_permissions'
    )

    def __str__(self):
        return f"{self.transaction_type} - {self.transaction_id} - {self.username}"
