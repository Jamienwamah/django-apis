from django.db import models
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

class FAQ(models.Model):
    # Define AES encryption key
    AES_KEY = get_random_bytes(16)

    # Encrypted fields
    encrypted_question = models.BinaryField(default=b'')
    encrypted_answer = models.BinaryField(default=b'')

    def __str__(self):
        return self.get_decrypted_question()

    def encrypt_field(self, data):
        cipher = AES.new(self.AES_KEY, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        return b64encode(ct_bytes)

    def decrypt_field(self, encrypted_data):
        cipher = AES.new(self.AES_KEY, AES.MODE_CBC)
        pt = unpad(cipher.decrypt(b64decode(encrypted_data)), AES.block_size)
        return pt.decode('utf-8')

    def get_decrypted_question(self):
        return self.decrypt_field(self.encrypted_question)

    def get_decrypted_answer(self):
        return self.decrypt_field(self.encrypted_answer)

    def set_encrypted_question(self, question):
        self.encrypted_question = self.encrypt_field(question)

    def set_encrypted_answer(self, answer):
        self.encrypted_answer = self.encrypt_field(answer)

    def save(self, *args, **kwargs):
        self.set_encrypted_question(self.question)
        self.set_encrypted_answer(self.answer)
        super().save(*args, **kwargs)
