# Generated by Django 5.0.1 on 2024-02-12 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0029_alter_otp_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp_code',
            field=models.CharField(default='0278', max_length=6),
        ),
    ]
