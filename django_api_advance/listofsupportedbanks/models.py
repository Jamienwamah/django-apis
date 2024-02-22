from django.db import models
import uuid

class SupportedBank(models.Model):
    id = models.CharField(primary_key=True, max_length=32, editable=False)  # Custom ID field
    name = models.CharField(max_length=255)
    local_reference = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate the ID from the list of API keys provided by Watu
        self.id = self.generate_id_from_api_key()

        # Call the super method to save the model instance
        super().save(*args, **kwargs)

    def generate_id_from_api_key(self):
        # Generate a unique ID using UUID
        generated_id = uuid.uuid4().hex
        return generated_id
