from django.db import models

class Announcement(models.Model):
    body = models.TextField()  # Store plain text body if needed
    date = models.DateTimeField(auto_now_add=True)
    encrypted_body = models.CharField(max_length=500, default='')  # Store encrypted body if needed
    jwt_token = models.CharField(max_length=500, default='')  # Store JWT token for authentication/authorization

    def __str__(self):
        return f"{self.date}: {self.body}"
