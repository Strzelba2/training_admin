# Generated by Django 3.0.6 on 2020-05-13 20:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Szkolenie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NewTraining', models.CharField(max_length=200)),
                ('DateTraining', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('subname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('adress', models.TextField(max_length=400)),
                ('invoice', models.BooleanField(verbose_name='Proszę o wystawienie faktury')),
                ('name_company', models.CharField(blank=True, max_length=100, null=True)),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('NIP', models.CharField(blank=True, max_length=200, null=True)),
                ('street', models.CharField(blank=True, max_length=200, null=True)),
                ('zip', models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.RegexValidator(message='musi  być zachowany format  12-123', regex='[0-9]{2}[-]{1}[0-9]{3}')])),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('statement', models.BooleanField(verbose_name='„Oświadczam, że zakupiona usługa szkoleniowa mająca charakter usługi kształcenia/przekwalifikowania zawodowego, jest finansowana ze środków publicznych w całości zgodnie z treścią art. 43 ust. 1 pkt 29 lit. c ustawy z dnia 11.03.2004 o podatku od towarów i usług (Dz. U. Nr 54, poz. 535 ze zm.) / w co najmniej 70%, zgodnie z treścią § 13 ust. 1 pkt 20 rozporządzenia Ministra Finansów z dnia 04.04.2011 r. w sprawie wykonania niektórych przepisów ustawy o podatku od towarów i usług (Dz. U. Nr 73 poz. 392). W związku z tym proszę o wystawienie faktury VAT ze zwolnioną stawką podatku.”')),
                ('cost', models.FloatField(blank=True, max_length=800, null=True)),
                ('comments', models.TextField(blank=True, max_length=800, null=True)),
                ('agreement', models.BooleanField(verbose_name='Zgadzam się na przetwarzanie moich danych osobowych przez Stowarzyszenie Bibliotekarzy Polskich Zarząd Główny zgodnie z ustawą o Ochronie Danych Osobowych z 10 maja 2018 r. Dz. Ust. 2018 poz. 1000., w celach związanych z organizacją konferencji. ')),
                ('NewTraining', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.Szkolenie')),
            ],
        ),
    ]