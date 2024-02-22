from django.contrib.auth.backends import BaseBackend
from .models import User

class CustomUserAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
        return None
