from django.shortcuts import render, redirect,reverse
from django.contrib.auth import login, get_user_model, logout
from random import randint
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from .models import MyUsers
from django.db.models import Q
import time
from django.utils import timezone


from .forms import UserCreationForm, UserLoginForm , RegisterNumForm


def register(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user=form['email'].value()
        num = randint(10000, 60000)
        mess = f'Numer do weryfikacji:{str(num)}'
        subject = "random numbers"
        email_user = settings.EMAIL_HOST_USER
        emails = [user]
        msg = EmailMessage(subject, mess, email_user, emails)
        msg.send()
        form.save()
        user = MyUsers.objects.get(email= user)
        user.random_number=num
        user.save()
        return redirect('registerNum',str(user))
        
    context = {
        'form': form

    }
    return render(request, "register.html", context)


def login_view(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        user_login = form.cleaned_data.get('query')
        user = MyUsers.objects.filter(
				Q(username__iexact=user_login) |
				Q(email__iexact=user_login)
			).distinct()
        username = user[0]
        return redirect(f"/panel/list/{username}")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/login")

def registerNum_view(request,*args, **kwargs):
    user = kwargs.get('user')
    num = MyUsers.objects.get(username= user).random_number
    register_try = MyUsers.objects.get(username= user).register_try
    if register_try == None:
        register_try = 1
    else:
        register_try += 1
    user_obj= MyUsers.objects.filter(username= user)
    user_obj.update(register_try=register_try)
    date_join = MyUsers.objects.get(username= user).date_joined
    now = timezone.now()
    dt= now - date_join

    if dt.seconds <= 180 and register_try <= 3:
    
        form = RegisterNumForm(request.POST or None,randoNumUser=num)
        
        if form.is_valid():
            randomNum = form.cleaned_data.get('RandomNUM')
            user_num = MyUsers.objects.filter(random_number=randomNum)
            
            email = MyUsers.objects.get(username= user).email

            mess = 'Dziękujemy za rejestracjię'
            subject = "potwierdzenie rejestracji"
            email_user = settings.EMAIL_HOST_USER
            emails = [email]
            msg = EmailMessage(subject, mess, email_user, emails)
            msg.send()
            user_num.update(is_active=True,random_number= None)
            return redirect("/login")
        return render(request,"registerNum.html/",{"form":form,"usernum":user})
    else:
        user = MyUsers.objects.get(username= user)
        user.delete()

        error = "czas minoł lub liczba prób przekroczyła 3"
        return render(request,'error.html',{"error":error})

