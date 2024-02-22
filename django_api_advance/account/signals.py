# user_profile/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from rent.models import User  # Import User model

@receiver(post_save, sender=User)
def additional_processing(sender, instance, created, **kwargs):
    if created:
        # Additional processing for newly created UserProfile
        pass

