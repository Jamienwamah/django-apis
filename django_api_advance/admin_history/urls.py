from django.urls import path
from .views import AdminHistoryView

urlpatterns = [
    path('admin-history/', AdminHistoryView.as_view(), name='admin_history'),
]
