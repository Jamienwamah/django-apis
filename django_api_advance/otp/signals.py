from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rent.models import User
from forpass.models import Forgot
from .models import OTP
from django.core.mail import send_mail
from django.utils import timezone

@receiver(post_save, sender=User) 
def create_token(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        otp = OTP.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
        instance.is_active = False 
        instance.save()
        
        send_otp_email(instance, otp)

def send_otp_email(user, otp):
    subject = "Email Verification"
    message = f"""
    Dear {user.username},
    
    this one time otp code is a confirmation that your email has been verified successfully, please proceed to login:
    
    Verification Code: {otp.otp_code}
    
    
    Thank you!
    """
    from_email = "rentspacedev@gmail.com"
    receiver_email = [user.email]
    
    send_mail(
        subject,
        message,
        from_email,
        receiver_email,
        fail_silently=False,
    )

    





