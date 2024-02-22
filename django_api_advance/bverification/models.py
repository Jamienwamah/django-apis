from django.db import models

class BVNVerification(models.Model):
    bvn = models.CharField(max_length=11, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"BVN: {self.bvn}, Verified: {self.is_verified}"
