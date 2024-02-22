"""
URL configuration for RentSpace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from login.views import LoginAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# List of app URLs to include dynamically
app_urls = [
    'rent.urls',
    'account.urls',
    'admin_control.urls',
    'admin_history.urls',
    'announcement.urls',
    'landlord.urls',
    'maintenance.urls',
    'pverification.urls',
    'loandebit.urls',
    'chat.urls',
    'cardverification.urls',
    'otp.urls',
    'kyc.urls',
    # 'dva.urls',
    'loancreation.urls',
    'wallet.urls',
    'bverification.urls',
    'accountdetails.urls',
    'adebitting.urls',
    'activities.urls',
    'listofsupportedbanks.urls',
    # 'dva.urls',
    # 'dva_history.urls',
    #'login.urls',
    'reset.urls',
    'forpass.urls',
    'notification.urls',
    'bdebit.urls',
    # 'user_activities.urls',
    'space_rent_creation.urls',
    # 'bvn.urls',
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Include app URLs dynamically
for app_url in app_urls:
    urlpatterns.append(path('api/v1/', include(app_url)))

# Define a router for user-related views
router = DefaultRouter()
#router.register('user', LoginAPIView, basename='user')

# Add user-related URLs to urlpatterns
urlpatterns += router.urls
