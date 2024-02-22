import random
import string
from django.conf import settings
from otp.models import OTP
from twilio.rest import Client

def generate_otp(length=6):
    characters = string.digits
    