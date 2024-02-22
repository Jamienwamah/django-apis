from django.db import models

class AdminHistory(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('other', 'Other'),
    ]

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    email = models.CharField(max_length=255)  # Store encrypted email if needed
    user_id = models.PositiveIntegerField()
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(blank=True, null=True)
    role = models.CharField(max_length=50)  # Store encrypted role if needed
    session_id = models.CharField(max_length=100)  # Store encrypted session ID if needed
    jwt_token = models.CharField(max_length=255, default='')


    def __str__(self):
        return f"{self.action} - {self.email}"
