from django.db import models

class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, default='')
    aes_key = models.CharField(max_length=255, default='')   # Field to store AES key
    jwt_token = models.CharField(max_length=255, default='')  # Field to store JWT token

    def __str__(self):
        return self.title
