# Generated by Django 3.0.6 on 2020-09-29 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0010_message_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='message_email',
            name='inpFileImage',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
