# Generated by Django 5.0.1 on 2024-02-12 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dva', '0002_alter_virtualaccount_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualaccount',
            name='customer_email',
            field=models.EmailField(max_length=254),
        ),
    ]
