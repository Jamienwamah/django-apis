# Generated by Django 5.0.1 on 2024-02-08 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0017_alter_otp_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp_code',
            field=models.CharField(default='939430', max_length=6),
        ),
    ]