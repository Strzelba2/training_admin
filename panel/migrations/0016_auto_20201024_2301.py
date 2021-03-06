# Generated by Django 3.0.6 on 2020-10-24 21:01

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0015_auto_20201018_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panel',
            name='email_user',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='panel',
            name='phoneNumber',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
