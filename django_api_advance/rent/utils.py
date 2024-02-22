import random
import string
from django.core.mail import send_mail

def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_otp_email(email, otp):
    """Send OTP to the user's email address."""
    subject = 'OTP for registration'
    message = f'Your OTP for registration is: {otp}'
    from_email = 'your@example.com'  # Update with your email address
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
