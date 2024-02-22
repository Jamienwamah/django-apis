# Generated by Django 5.0.1 on 2024-02-02 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space_rent_creation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spacerentprofile',
            name='space_rent_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='spacerentprofile',
            name='encrypted_data',
            field=models.BinaryField(),
        ),
    ]
