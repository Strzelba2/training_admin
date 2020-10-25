from __future__ import unicode_literals
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
import os
import shutil




class Szkolenie(models.Model):
    NewTraining = models.CharField( max_length=200)
    DateTraining = models.DateField( auto_now=False, auto_now_add=False)
    Provider = models.CharField( max_length=200, )
    max_participants = models.IntegerField( )
    archiwum = models.BooleanField(default=False)

    def __str__(self):
        return self.NewTraining

class send_email_message(models.Model):
    name_message_send = models.ForeignKey("Message_email",on_delete=models.CASCADE)
    neme_user_send = models.ForeignKey("Panel",on_delete=models.CASCADE)
    send_email = models.BooleanField(default=True)




class Panel (models.Model):
    NewTraining = models.ForeignKey("Szkolenie",  on_delete=models.CASCADE )
    name_user = models.CharField( max_length=50)
    subname = models.CharField( max_length=50)
    email_user = models.EmailField( max_length=254)
    phoneNumber = PhoneNumberField()
    adress = models.TextField(max_length=400)
    invoice = models.BooleanField("Proszę o wystawienie faktury" )
    name_company = models.CharField( max_length=100 , blank=True, null=True)
    full_name_company = models.CharField(max_length=100 , blank=True, null=True)
    NIP = models.CharField( max_length=200, blank=True, null=True)
    street = models.CharField( max_length=200, blank=True, null=True)
    zip = models.CharField( max_length=200, 
    validators=[
        RegexValidator(
        regex=r'[0-9]{2}[-]{1}[0-9]{3}',
        message='musi  być zachowany format  12-123',
    )],
    blank=True,
    null=True
    )
    city = models.CharField( max_length=200, blank=True, null=True)
    statement = models.BooleanField("„Oświadczam, że zakupiona usługa szkoleniowa mająca charakter usługi kształcenia/przekwalifikowania zawodowego, jest finansowana ze środków publicznych w całości zgodnie z treścią art. 43 ust. 1 pkt 29 lit. c ustawy z dnia 11.03.2004 o podatku od towarów i usług (Dz. U. Nr 54, poz. 535 ze zm.) / w co najmniej 70%, zgodnie z treścią § 13 ust. 1 pkt 20 rozporządzenia Ministra Finansów z dnia 04.04.2011 r. w sprawie wykonania niektórych przepisów ustawy o podatku od towarów i usług (Dz. U. Nr 73 poz. 392). W związku z tym proszę o wystawienie faktury VAT ze zwolnioną stawką podatku.”" )
    cost = models.FloatField(max_length=800, blank=True, null=True )
    comments = models.TextField(max_length=800, blank=True, null=True)
    agreement = models.BooleanField("Zgadzam się na przetwarzanie moich danych osobowych przez Stowarzyszenie Bibliotekarzy Polskich Zarząd Główny zgodnie z ustawą o Ochronie Danych Osobowych z 10 maja 2018 r. Dz. Ust. 2018 poz. 1000., w celach związanych z organizacją konferencji. " )
    
    def get_absolute_url(self):
        return reverse('panel')

    def __str__(self):
        return self.name_user

class Message_email (models.Model):
    name_message = models.CharField( max_length=100,unique=True )
    text_message = models.TextField()
    

    def __str__(self):
        return self.name_message

@receiver(models.signals.post_delete, sender=Message_email)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    path = settings.MEDIA_ROOT+'\\'+f'{instance.name_message}'
    
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
