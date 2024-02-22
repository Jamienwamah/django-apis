# Generated by Django 5.0.1 on 2024-02-12 12:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dva', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='virtualaccount',
            options={'verbose_name': 'Virtual Account', 'verbose_name_plural': 'Virtual Accounts'},
        ),
        migrations.RenameField(
            model_name='virtualaccount',
            old_name='customer_name',
            new_name='account_name',
        ),
        migrations.RenameField(
            model_name='virtualaccount',
            old_name='balance',
            new_name='business_wallet_id',
        ),
        migrations.RemoveField(
            model_name='virtualaccount',
            name='created_at',
        ),
        migrations.AddField(
            model_name='virtualaccount',
            name='bank',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='virtualaccount',
            name='customer_email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='virtualaccount',
            name='customer_id',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='virtualaccount',
            name='customer_id_type',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='virtualaccount',
            name='customer_phone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='virtualaccount',
            name='institution_reference',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='virtualaccount',
            name='prefix',
            field=models.CharField(default='', max_length=10),
        ),
    ]