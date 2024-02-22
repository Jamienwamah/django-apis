from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rent.models import User
import random
import string
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode, b64decode

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=''.join([str(random.randint(0, 9)) for _ in range(4)]))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    encrypted_otp = models.TextField(blank=True, null=True)
    expiration_time = models.DateTimeField(blank=True, null=True)

    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=4))

    def generate_and_encrypt_otp(self):
        otp = self.generate_otp()
        self.encrypted_otp = self.encrypt_otp(otp)
        self.expiration_time = timezone.now() + timezone.timedelta(minutes=5)  # OTP expires in 5 minutes
        self.save()
        return otp

    def verify_otp(self, otp):
        decrypted_otp = self.decrypt_otp()
        return decrypted_otp == otp and timezone.now() <= self.expiration_time

    def encrypt_otp(self, otp):
        backend = default_backend()
        cipher = Cipher(algorithms.AES(settings.SECRET_KEY[:32].encode()), modes.CBC(b'\x00' * 16), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(otp.encode()) + padder.finalize()
        encrypted_otp = encryptor.update(padded_data) + encryptor.finalize()
        return b64encode(encrypted_otp).decode()

    def decrypt_otp(self):
        backend = default_backend()
        cipher = Cipher(algorithms.AES(settings.SECRET_KEY[:32].encode()), modes.CBC(b'\x00' * 16), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = decryptor.update(b64decode(self.encrypted_otp)) + decryptor.finalize()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data.decode()
