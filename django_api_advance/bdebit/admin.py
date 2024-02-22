from django.contrib import admin
from django.contrib.admin import site
from django.contrib.admin.models import LogEntry
from bdebit.models import BvnDebitUser

admin.site.register(BvnDebitUser)
admin.site.register(LogEntry)
#admin.site.register(BvnDebitDetails)

#site.unregister(LogEntry)
#site.register(CustomLogEntry)