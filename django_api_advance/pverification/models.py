from django.db import models
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from django.conf import settings
import random
import string

class PhoneVerification(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    encrypted_verification_code = models.CharField(max_length=255, default='')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_verification_code():
        return ''.join(random.choices(string.digits, k=6))

    def encrypt_verification_code(self, verification_code):
        aes_cipher = AES.new(settings.SECRET_KEY[:32], AES.MODE_CBC)
        encrypted_code = aes_cipher.encrypt(pad(verification_code.encode(), AES.block_size))
        return b64encode(encrypted_code).decode()

    def decrypt_verification_code(self):
        aes_cipher = AES.new(settings.SECRET_KEY[:32], AES.MODE_CBC)
        decrypted_code = unpad(aes_cipher.decrypt(b64decode(self.encrypted_verification_code)), AES.block_size)
        return decrypted_code.decode()

    def save(self, *args, **kwargs):
        if not self.pk:
            verification_code = self.generate_verification_code()
            self.encrypted_verification_code = self.encrypt_verification_code(verification_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Phone: {self.phone_number}, Verified: {self.is_verified}"
