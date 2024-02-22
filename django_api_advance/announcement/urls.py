from django.urls import path
from .views import AnnouncementListView

urlpatterns = [
    path('announcements/', AnnouncementListView.as_view(), name='announcement-list'),
]
