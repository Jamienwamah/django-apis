from django.urls import path
from accountdetails.views import get_user_account_details

urlpatterns = [
    path('accountdetails/', get_user_account_details, name='get-user-account-details'),
]
