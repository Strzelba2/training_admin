# Generated by Django 3.0.6 on 2020-10-04 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0011_message_email_inpfileimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message_email',
            name='inpFileImage',
        ),
        migrations.AlterField(
            model_name='message_email',
            name='name_message',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
