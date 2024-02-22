from django.urls import path
from rent.views import CustomUserAPIView, LoginAPIView, UserAPIView, RefreshAPIView, LogoutAPIView


urlpatterns = [
    path('auth/register/', CustomUserAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('refresh/', RefreshAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view())
   # path('auth/login/', LoginUserView.as_view(), name='login'),
]