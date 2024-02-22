from django.db import models
from loancreation.models import CustomerLoan  # Assuming CustomerLoan is defined in loancreation app

class Loan(models.Model):
    customer = models.ForeignKey(CustomerLoan, on_delete=models.CASCADE)  # Corrected reference
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields as needed

class Debit(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields as needed
