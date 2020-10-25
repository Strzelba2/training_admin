from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.conf import settings
import random
import os
from django.dispatch import receiver
from django.core.exceptions import ValidationError

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'
def validate_image(image):
    file_size = image.file.size
    limit_kb = 2*1024
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is 2 MB" )
    return image
def path_file_name(instance, filename):
    return settings.MEDIA_ROOT+'\\{username}{random}.jpg'.format(
        username=instance.username, random=random.randint(0,100000))

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, username, email,password=None, **extra_fields):
        extra_fields.setdefault("is_active",False)
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_admin",False)
        extra_fields.setdefault("is_superuser",False)

        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have an password')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email, password=None ,**extra_fields):
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_admin",True)
        extra_fields.setdefault("is_superuser",True)
        user = self.create_user(
            username=username,
            password=password,
            email=email,
            **extra_fields,
        )
        
        user.save(using=self._db)
        return user

class MyUsers(AbstractBaseUser):
    username = models.CharField(
        max_length=300,
        validators=[
            RegexValidator(regex=USERNAME_REGEX,
                           message='Username must be alphanumeric or contain numbers',
                           code='invalid_username'
                           )],
        unique=True
    )
    full_name = models.CharField(max_length=50, blank=True, null=True)
    date_joined = models.DateTimeField( auto_now_add=True)
    last_login = models.DateTimeField(blank=True,null=True)
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='email address'
    )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    random_number = models.IntegerField(default= None, blank=True, null=True)
    register_try = models.IntegerField(default= None, blank=True, null=True)
    
    image = models.ImageField('Image',upload_to=path_file_name,blank=True, null=True, validators=[validate_image])

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True


    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "\\static\\img\\avatar.jpg"

@receiver(models.signals.post_delete, sender=MyUsers)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """

    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=MyUsers)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False
    new_file = instance.image
    if not  old_file == "":
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

            

  
