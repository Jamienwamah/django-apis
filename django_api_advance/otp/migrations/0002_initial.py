# Generated by Django 5.0.1 on 2024-02-06 07:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otp', '0001_initial'),
        ('rent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otps', to='rent.user'),
        ),
    ]
