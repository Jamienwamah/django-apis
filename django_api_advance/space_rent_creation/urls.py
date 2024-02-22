from django.urls import path
from .views import SpaceRentProfileCreateView, SpaceRentProfileRetrieveUpdateView

urlpatterns = [
    path('space-rent/create/', SpaceRentProfileCreateView.as_view(), name='create-space-rent'),
    path('space-rent/', SpaceRentProfileRetrieveUpdateView.as_view(), name='retrieve-update-space-rent'),
]
