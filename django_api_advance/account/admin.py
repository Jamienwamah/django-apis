from django.contrib import admin
from .models import AccountUser

# Register your models here.


class AccountUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'gender', 'status', 'wallet_address', 'has_dva', 'has_rent')
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'wallet_address')
    readonly_fields = ['loan_amount',]
    writeonly_fields = ['password',]
    list_filter = ('gender',)

admin.site.register(AccountUser, AccountUserAdmin)



