# Generated by Django 3.0.6 on 2020-09-23 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0009_auto_20200921_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message_email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_message', models.CharField(max_length=100)),
                ('text_message', models.TextField()),
            ],
        ),
    ]