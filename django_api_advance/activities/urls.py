# activities/urls.py
from django.urls import path
from .views import ActivityList

urlpatterns = [
    path('activities/', ActivityList.as_view(), name='activity-list'),
]
