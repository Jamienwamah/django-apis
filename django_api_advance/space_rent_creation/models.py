from django.db import models
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from datetime import datetime

class SpaceRentProfile(models.Model):
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    savings_interval = models.CharField(max_length=100)
    space_rent_id = models.IntegerField(default=0)
    encrypted_data = models.BinaryField()

    def encrypt_data(self, encryption_key):
        cipher = AES.new(encryption_key.encode(), AES.MODE_CBC)
        data = f"{self.rent_amount},{self.due_date},{self.created_at},{self.savings_interval},{self.space_rent_id}"
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        self.encrypted_data = ct_bytes

    def decrypt_data(self, encryption_key):
        cipher = AES.new(encryption_key.encode(), AES.MODE_CBC)
        pt = unpad(cipher.decrypt(self.encrypted_data), AES.block_size)
        decrypted_data = pt.decode()
        rent_amount, due_date_str, created_at_str, savings_interval, space_rent_id = decrypted_data.split(',')
        self.rent_amount = float(rent_amount)
        self.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        self.created_at = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')
        self.savings_interval = savings_interval
        self.space_rent_id = int(space_rent_id)

    def save(self, *args, **kwargs):
        if not self.id:
            # Assuming `encryption_key` is provided when saving
            self.encrypt_data(kwargs.pop('encryption_key', ''))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Space Rent Profile - {self.id}"

    class Meta:
        verbose_name_plural = "Space Rent Profiles"
