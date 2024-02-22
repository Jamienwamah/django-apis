from django.db import models
from listofsupportedbanks.models import SupportedBank

class VirtualAccount(models.Model):
    account_name = models.CharField(max_length=100)
    business_wallet_id = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Define a ForeignKey field to link to the SupportedBank model
    bank = models.ForeignKey(SupportedBank, on_delete=models.CASCADE)

    # Additional fields
    prefix = models.CharField(max_length=10, default='')
    customer_email = models.EmailField()  # Required field, already validated by EmailField
    customer_id = models.CharField(max_length=11, default='')  # BVN number should be 11 digits
    customer_id_type = models.CharField(max_length=50, default='')  # Customer ID type used
    institution_reference = models.CharField(max_length=100, default='')  # Reference to identity with on user's platform
    customer_phone = models.CharField(max_length=15, default='')  # Adjust max length as needed

    class Meta:
        verbose_name = "Virtual Account"
        verbose_name_plural = "Virtual Accounts"

    def __str__(self):
        return self.account_name
