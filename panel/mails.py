from django.conf import settings
from django.core.mail import EmailMessage , send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string ,get_template
from django.shortcuts import render,reverse,get_object_or_404,redirect
from email.mime.image import MIMEImage
from .models import Panel , Szkolenie,Message_email,send_email_message
from django.utils.safestring import mark_safe
from django.template import loader, Context

def send_active(email,name,szkolenie,**kwargs):

        szkolenie = szkolenie
        txt_message = render_to_string('text_email.txt')
        subject=f'Poprawna rejestacja na Szkolenie: {szkolenie}'

        email_user = settings.EMAIL_HOST_USER

        email=[email]
        msg = EmailMessage(subject,txt_message,email_user,email)
        msg.send()


def send_message_user(message,emails,szkolenie,**kwargs):
        message=message
        email_user = settings.EMAIL_HOST_USER
        emails = emails
        szkolenie = szkolenie
        subject=message
        message_txt = Message_email.objects.get(name_message=message).text_message 

        dict_image={}
        x=message_txt.split('<')
        for i in x:
                if 'img' in i:
                        img=i.rsplit(' ',8)
                        dict_image[img[2][4:-1]]=img[0][15:-1]
                        image_cid = f"cid:{img[2][4:-1]}"
                        message_txt=message_txt.replace(img[0][9:-1],image_cid)
                        message_txt = message_txt.replace("cursor: pointer;", '')

        d = { 'message': message_txt ,"static": "http://{}{}".format(
                "127.0.0.1:8000/",
                settings.STATIC_URL),}
        d.update(kwargs.get("context", {}))

        html_message = get_template('email.html').render(d)
        msg = EmailMultiAlternatives(subject,message_txt,email_user,emails)
        msg.attach_alternative(html_message, "text/html") 
        msg.mixed_subtype = 'related'

        for id_img, src in dict_image.items():

                path_to = settings.MEDIA_ROOT+src
                with open(path_to, 'rb') as f:
                        logo_file = f.read()
                logo_mime = MIMEImage(logo_file)

                logo_mime.add_header('Content-ID', f'<{id_img}>')
                msg.attach(logo_mime)

        msg.send()
        for email in emails:
                list_user_sent = Panel.objects.get(email_user = email)
                list_message_sent = Message_email.objects.get(name_message =message)
                send_email = send_email_message(name_message_send=list_message_sent,neme_user_send = list_user_sent )
                send_email.save()



        
        


        
        
        


        
        

 
                     
