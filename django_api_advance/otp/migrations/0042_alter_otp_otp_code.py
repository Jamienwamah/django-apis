# Generated by Django 5.0.1 on 2024-02-13 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0041_alter_otp_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp_code',
            field=models.CharField(default='5020', max_length=6),
        ),
    ]