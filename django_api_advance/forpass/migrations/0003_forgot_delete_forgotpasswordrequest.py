# Generated by Django 5.0.1 on 2024-02-11 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forpass', '0002_remove_forgotpasswordrequest_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forgot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password_reset_token', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='ForgotPasswordRequest',
        ),
    ]
