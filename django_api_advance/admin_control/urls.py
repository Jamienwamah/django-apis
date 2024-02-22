from django.urls import path
from .views import UserStatusView

urlpatterns = [
    path('user-status/', UserStatusView.as_view(), name='user-status'),
]
