from django.contrib import admin
from .models import Panel, Szkolenie,Message_email,send_email_message

# Register your models here.

admin.site.register(Panel)
admin.site.register(Szkolenie)
admin.site.register(Message_email)
admin.site.register(send_email_message)