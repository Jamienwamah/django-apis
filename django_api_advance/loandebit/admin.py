from django.contrib import admin
from .models import Loan, Debit

# Register your models here.
admin.site.register(Debit)
admin.site.register(Loan)