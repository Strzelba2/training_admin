# Generated by Django 3.0.6 on 2020-10-18 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0013_szkolenie_archiwum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panel',
            name='sent',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
