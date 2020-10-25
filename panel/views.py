from django.shortcuts import render,reverse,redirect
from .models import Panel , Szkolenie,Message_email,send_email_message
from django.forms import CharField,FileInput
from MyUser.models import MyUsers
from MyUser.forms import UserCreationForm
from django.views.generic import ListView 
from django.views.generic.edit import CreateView , DeleteView,UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from .forms import userslist , Szkolenielist
from django.conf import settings
from random import randint
from django.template import Context
from.mails import send_active , send_message_user
from django.core.files.uploadedfile import SimpleUploadedFile ,UploadedFile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect,HttpResponse
from django import forms
from django.core.exceptions import ValidationError
import pandas as pd
from django.db.models import Q
import os
import re



def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper

# Create your views here.
@superuser_required()
class PanelListView(ListView):
    
    model = Panel
    fields = []
    template_name = "panel.html"
    
    def get(self, request, *args, **kwargs):
        
        search = request.GET.get("search_id")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        search = self.request.GET.get("search_id")
        if search == None or search == "":
            search_qs_Panel = None
        else:
            try:
                search_qs_Panel = Panel.objects.filter(
                    Q(name_user__icontains=search) |
                    Q(subname__icontains=search) |
                    Q(email_user__icontains=search)|
                    Q(phoneNumber__icontains=search)|
                    Q(adress__icontains=search)|
                    Q(NIP__icontains=search)|
                    Q(city__icontains=search)
                ).distinct()
            except:
                search_qs_Panel = False
            if not search_qs_Panel :   
                search_qs_Panel = False
        context = super().get_context_data(**kwargs)
        context["search"]=search_qs_Panel
        context['send'] = send_email_message.objects.all()
      
        return context

class formularz (CreateView):
    model = Panel
    form_class = userslist
    template_name = "formularz.html"

    def get_success_url(self ):
        email =  self.request.POST.get("email_user")
        name =  self.request.POST.get("name_user")
        return reverse('corectForm', kwargs={'email':email,'name':name})

    def form_valid(self, form):

        newtrening= self.request.POST.get('NewTraining')
        szkolenie = Szkolenie.objects.get(pk = newtrening ).NewTraining
        email = form.cleaned_data['email_user']
        name = form.cleaned_data['name_user']
        try:
            send_active(email,name,szkolenie)
        except:
            
            email = form.cleaned_data.get("email_user")
            msg = "podany adres jest nie prawidłowy, lub istnieje w bazie danych"
            form.add_error('email_user', msg)

            return super().form_invalid(form) 
               
        return super().form_valid(form)
    def form_invalid(self, form):


        return super().form_invalid(form)  
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_training'] = Szkolenie.objects.all()
        return context

def correct_form (request ,email,name):

    email=str(email)
    name=str(name)
    return render(request,"correct_form.html",{"email":email,"name":name})

def email(request ):

    return render(request,'email.html')


@superuser_required()
class ListaSzkolenView(ListView):
    model = Szkolenie
    fields = []
    template_name = "listaSzkolen.html"
    context_object_name = "lista_szkolen"
    ordering = ['NewTraining',]
    
    def __init__(self, **kwargs):
        self.list_order = {'NewTraining':'-NewTraining','DateTraining':'-DateTraining','Provider':'-Provider'}
        self.class_sort =["fa fa-angle-down","fa fa-angle-down","fa fa-angle-down"]


    def get_queryset(self):
        ordering = self.get_ordering()
        if self.kwargs['szkolenie'] == "szkolenie":
            data = Szkolenie.objects.filter(archiwum=False).order_by(ordering)
        elif self.kwargs['szkolenie'] == "archiwum":
            
            data = Szkolenie.objects.filter(archiwum=True).order_by(ordering)
        return data
        
    def get_ordering(self):    
        self.ordering = self.request.GET.get("orderlist")
        
        
        if self.ordering == None: 
            self.ordering = next(iter(self.list_order)) 
        else: 
            if self.ordering in self.list_order:
                self.ordering = self.list_order.get(self.ordering,'')
            else:
                self.ordering=list(self.list_order.keys())[list(self.list_order.values()).index(self.ordering)]

        for i, item in enumerate(self.list_order.items()):
            if self.ordering in item[0]:
                self.class_sort[i] = "fa fa-angle-up"
            elif self.ordering in item[0]:
                self.class_sort[i] = "fa fa-angle-down"
                
        return  self.ordering
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.ordering in self.list_order:
            cont =list(self.list_order.keys())
        else :
            cont =list(self.list_order.values()) 
        if self.kwargs['szkolenie'] == "archiwum":
            archiwum = False
        else:
            archiwum = True

        context['actual_ordering'] = cont
        context['archiwum'] = archiwum
        context['class_sort'] = self.class_sort
        return context

@superuser_required()
class Create_szkolenie_view (CreateView):
    model = Szkolenie
    form_class = Szkolenielist
    template_name = "create_szkolenie.html"

    def get_success_url(self):
        user = self.request.user.username
        szkolenie = "szkolenie"
        return reverse("ListaSzkolenView",kwargs={'username':user,'szkolenie':szkolenie})

    def form_valid(self, form):

        return super().form_valid(form)
@superuser_required()
class update_szkolenie_view (UpdateView):
    model = Szkolenie
    fields = "__all__"
    template_name = 'update_szkolenie.html'

    def get_success_url(self):
        user = self.request.user.username
        szkolenie = self.kwargs['szkolenie']
        return reverse("ListaSzkolenView",kwargs={'username':user,'szkolenie':szkolenie})

    def form_valid(self, form):

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['szkolenie_data'] = Szkolenie.objects.all()
        return context

@user_passes_test(lambda u: u.is_superuser)   
def archiwum_Szkolenie(request , username , szkolenie):
    if request.method == "POST":
        for i in Szkolenie.objects.all():
            b=f'archiwum{i.pk}'
            x= request.POST.get(b)
        
            if x == "on" :
                archiwum_szkolenie=Szkolenie.objects.filter(pk=i.pk)
                archiwum_szkolenie.update(archiwum = True)

    user = request.user.username
    szkolenie = szkolenie
    return HttpResponseRedirect(reverse("ListaSzkolenView",kwargs={'username':user,'szkolenie':szkolenie}))

@user_passes_test(lambda u: u.is_superuser)
def delete_Szkolenie(request , username , szkolenie):

    if request.method == "POST":
        for i in Szkolenie.objects.all():
            b=f'check{i.pk}'
            x= request.POST.get(b)
        
            if x == "on" :
                del_szkolenie=Szkolenie.objects.filter(pk=i.pk)
                del_szkolenie.delete()
    username =str(username)
    szkolenie = "szkolenie"

    return HttpResponseRedirect(reverse("ListaSzkolenView",kwargs={'username':username,'szkolenie':szkolenie}))

@superuser_required()
class ListaUserView(ListView):
    model = MyUsers
    fields = '__all__'
    template_name = "lista_users.html"
    context_object_name = "lista_users"


class update_Users_view (UpdateView):
    model = MyUsers
    fields = ['username','password','full_name','email','is_admin','is_staff','is_active','is_superuser','image']
    template_name = 'update_MyUsers.html'
   
    
    def get_form(self):
        form = super(update_Users_view, self).get_form()
        form.fields['password'].widget.attrs.update({'readonly':'True',})
        #form.initial['password'] = 'POlska.21!'
        return form

    def get_success_url(self):
        user = self.request.user.username
        return reverse("ListaUserView",kwargs={'username':user,})
    
    def form_valid(self, form):
        password = form.cleaned_data.get("password")
        return super().form_valid(form)


class Create_User_view (CreateView):
    model = MyUsers
    form_class = UserCreationForm
    template_name = "create_User.html"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.path_image=''


    
    def get_success_url(self):
        user = self.request.user.username
        return reverse("ListaUserView",kwargs={'username':user,})


    def get_context_data(self, **kwargs):
        data = super(Create_User_view, self).get_context_data(**kwargs)

        if self.path_image == 'error':
            pass
        else:
            if self.request.FILES:
                if self.path_image != '':
                    if not self.request.POST._mutable:
                        self.request.POST._mutable = True
                        self.request.POST['image_path'] = self.path_image
                        self.request.POST._mutable = False

        text_file = (self.request.POST, self.request.FILES)
        data['files'] = text_file

        return data
        
    def form_valid(self, form):
        
        if form.cleaned_data['image_path'] != '':
            from django.core.files.uploadedfile import SimpleUploadedFile
            image_path_to_save =settings.MEDIA_ROOT+'\\'+form.cleaned_data['image_path']
            file_data = {'image': SimpleUploadedFile(name=form.cleaned_data['image_path'], content=open(image_path_to_save, 'rb').read(), content_type='image/jpeg')}
            form = UserCreationForm(self.request.POST,file_data)
            delate_file = default_storage.delete(f'tmp/{file_data["image"].name}')
 
        return super().form_valid(form)

    def form_invalid(self, form):
        if "image" in form.errors:
            self.path_image='error'

        else:
            if self.request.FILES :
                uploaded_file = self.request.FILES['image']
                path = default_storage.save(f'tmp/{uploaded_file}', ContentFile(uploaded_file.read()))
                form.fields['image_path'].widget.attrs.update({'value':f'tmp\\{uploaded_file}'})
                self.path_image = f'tmp\\{uploaded_file}'

                
            if form.cleaned_data['image_path'] != '':

                self.path_image = form.cleaned_data['image_path']

        return super().form_invalid(form)

    def get_form(self):
        form = super(Create_User_view, self).get_form()
        
        return form

@user_passes_test(lambda u: u.is_superuser)
def delete_User(request , username):

    if request.method == "POST":
        for i in MyUsers.objects.all():
            b=f'check{i.pk}'
            x= request.POST.get(b)
        
            if x == "on" :
                del_User=MyUsers.objects.filter(pk=i.pk)
                del_User.delete()
        username =str(username)

    
    return redirect("ListaUserView",username=username)

@superuser_required()
class ListaSzkolenUsersView(ListView):
    model = Panel
    fields = []
    queryset = []
    template_name = "listaPanel.html"
    context_object_name = "listaPanel"
  
    def get_queryset(self):

        if self.kwargs['szkolenie'] == "bez":
            listaPanel = self.model.objects.all()
        else:
            szkolenie = Szkolenie.objects.get(NewTraining=self.kwargs['szkolenie'])
            listaPanel = self.model.objects.filter(NewTraining=szkolenie.pk)

        return listaPanel
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_training'] = Szkolenie.objects.all()
        context['archiwum'] = Szkolenie.objects.filter(archiwum=False)
        context['send'] = send_email_message.objects.all()
        context['message'] = Message_email.objects.all()
        context['szkolenie_cont'] = self.kwargs['szkolenie']
        return context

@user_passes_test(lambda u: u.is_superuser)
def delete_Userszkolenie(request , username , szkolenie ):
    if request.method == "POST":
        for i in Panel.objects.all():
            b=f'check{i.pk}'
            x= request.POST.get(b)

            if x == "on" :
                del_User=Panel.objects.filter(pk=i.pk)
                del_User.delete()
        username =str(username)
        szkolenie = str(szkolenie)

    
    return redirect("ListaSzkolenUsersView",username=username,szkolenie=szkolenie)  

@superuser_required()
class update_szkolenie_users (UpdateView):
    model = Panel
    fields = "__all__"
    template_name = 'update_szkolenie_user.html'
    

    def get_success_url(self):
        user = self.request.user.username
        szkolenie = self.kwargs['szkolenie']
        return reverse("ListaSzkolenUsersView",kwargs={'username':user,'szkolenie':szkolenie})

    def form_valid(self, form):

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        szkolenie = self.kwargs['szkolenie']
        context['szkolenie_data'] = Panel.objects.all()
        context['szkolenie_cont'] = szkolenie
        return context 

@user_passes_test(lambda u: u.is_superuser)
def convert_to_CSV(request , username , szkolenie):

    NewTraining =[]
    name_user = []
    subname = []
    email_user = []
    phoneNumber = []
    adress = []
    invoice = []
    name_company =[]
    full_name_company = []
    NIP = []
    street = []
    zip = []
    city = []
    statement = []
    cost = []
    comments =[]
    agreement = []

    if request.method == "POST":
        for i in Panel.objects.all():
            b=f'check{i.pk}'
            x= request.POST.get(b)

            if x == "on" :
                Panel_User=Panel.objects.filter(pk=i.pk)
                for e in Panel_User:
                    NewTraining.append(szkolenie)
                    name_user.append(e.name_user)
                    subname.append(e.subname)
                    email_user.append(e.email_user)
                    phoneNumber.append(e.phoneNumber)
                    adress.append(e.adress)
                    invoice.append(e.invoice)
                    name_company.append(e.name_company)
                    full_name_company.append(e.full_name_company)
                    NIP.append(e.NIP)
                    street.append(e.street)
                    zip.append(e.zip)
                    city.append(e.city)
                    statement.append(e.statement)
                    cost.append(e.cost)
                    comments.append(e.comments)
                    agreement.append(e.agreement)

        CSV_Szkolenie = {'Szkolenie': NewTraining,
        'Imię': name_user,
        'Nazwisko':subname,
        'Email':email_user,
        'Numer telefonu':phoneNumber,
        'adres':adress,
        'Faktura':invoice,
        'Nazwa Firmy':name_company,
        'Pełna Nazwa':full_name_company,
        'NIP':NIP,
        'Ulica':street,
        'Kod Pocztowy':zip,
        'Miasto':city,
        'Oświadczenie':statement,
        'Koszt':cost,
        'Komentarz':comments,
        'Zgoda':agreement,

        }
        df = pd.DataFrame(CSV_Szkolenie)
        username =str(username)
        szkolenie = str(szkolenie)

        try:

            from django.http import HttpResponse
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{username}_Lista.xlsx"'
            

            df.to_excel (response, index = False, header=True)
            
            return response
            
            
        except:
            return redirect("ListaSzkolenUsersView",username=username,szkolenie=szkolenie) 
    
    return redirect("ListaSzkolenUsersView",username=username,szkolenie=szkolenie) 

@superuser_required()
class MessageList(ListView):
    model = Message_email
    fields = "__all__"
    template_name = "list_message.html"
    context_object_name = "listamessage"

@user_passes_test(lambda u: u.is_superuser)
def delete_Message(request , username):

    if request.method == "POST":
        for i in Message_email.objects.all():
            b=f'check{i.pk}'
            x= request.POST.get(b)
        
            if x == "on" :
                del_message=Message_email.objects.filter(pk=i.pk)
                del_message.delete()
        username =str(username)
   
    return redirect("MessageList",username=username)

@superuser_required()    
class Create_Message (CreateView):
    model = Message_email
    fields = "__all__"
    template_name = "create_message.html"
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

    def get_success_url(self):
        user = self.request.user.username
        return reverse("MessageList",kwargs={'username':user,})
    def form_valid(self, form):
        
        self.object = form.save(commit=False)

        text_message =form.cleaned_data['text_message']
        message=form.cleaned_data['name_message']
        dict_image={}
        x=text_message.split('<')
        path = settings.MEDIA_ROOT+'\\'+f'{message}'

        if not os.path.exists(path):
            os.makedirs(path)

        for i in x:
                if 'img' in i:
                        img=i.rsplit(' ',8)
                        dict_image[img[2]]=img[0][4:]

        for filename, file in self.request.FILES.items():

            uploaded_file = self.request.FILES[filename]

            if  uploaded_file.name in os.listdir( path ) :

                rand = randint(10000, 90000)

                name = uploaded_file.name[:-4] + str(rand) + ".jpg"

                save_file = default_storage.save(f'{message}/{name}', ContentFile(uploaded_file.read()))
                image_path_to_save ='\\'+'media'+'\\'+f'{message}\\{name}'
                image_src = dict_image[ f'id="{filename}"']
                
                text_message=text_message.replace(image_src,f'src="{image_path_to_save}"',1)
                text_replace = f'name="{name}" id="{filename}"'
                text_to_replace = f'name="{uploaded_file.name}" id="{filename}"'
                text_message=text_message.replace(text_to_replace,text_replace,1)

            else:

                save_file = default_storage.save(f'{message}/{uploaded_file}', ContentFile(uploaded_file.read()))
                image_path_to_save ='\\'+'media'+'\\'+f'{message}\\{uploaded_file}'
                image_src = dict_image[ f'id="{filename}"']

                text_message=text_message.replace(image_src,f'src="{image_path_to_save}"',1)

        self.object.text_message = text_message
        self.object.save()
        

        return super().form_valid(form)

@superuser_required()
class update_Message_email (UpdateView):
    model = Message_email
    fields = "__all__"
    template_name = 'update_message_view.html'

    def get_success_url(self):
        user = self.request.user.username
        return reverse("MessageList",kwargs={'username':user,})
    
    def form_valid(self, form):
        self.object = form.save(commit=False)

        text_message =form.cleaned_data['text_message']
        message=form.cleaned_data['name_message']
        dict_image={}
        x=text_message.split('<')
        path = settings.MEDIA_ROOT+'\\'+f'{message}'
        dirs = os.listdir( path )
        list_image = []
        for i in x:
                if 'img' in i:
                        img=i.rsplit(' ',8)
                        dict_image[img[2]]=img[0][4:]
                        list_image.append(img[1])

        for filename, file in self.request.FILES.items():
            uploaded_file = self.request.FILES[filename]
            
            if  uploaded_file.name in dirs:

                rand = randint(10000, 90000)

                name = uploaded_file.name[:-4] + str(rand) + ".jpg"

                save_file = default_storage.save(f'{message}/{name}', ContentFile(uploaded_file.read()))
                image_path_to_save ='\\'+'media'+'\\'+f'{message}\\{name}'
                image_src = dict_image[ f'id="{filename}"']
                text_message=text_message.replace(image_src,f'src="{image_path_to_save}"')
                text_replace = f'name="{name}" id="{filename}"'
                text_to_replace = f'name="{uploaded_file.name}" id="{filename}"'
                text_message=text_message.replace(text_to_replace,text_replace,1)

            else:

                save_file = default_storage.save(f'{message}/{uploaded_file}', ContentFile(uploaded_file.read()))
                image_path_to_save ='\\'+'media'+'\\'+f'{message}\\{uploaded_file}'
                image_src = dict_image[ f'id="{filename}"']
                text_message=text_message.replace(image_src,f'src="{image_path_to_save}"')
    
        self.object.text_message = text_message
        self.object.save()

        for file_image in dirs:
            value= f'name="{file_image}"'
            if  value in list_image:
                continue
            else:
                path_to_delete = settings.MEDIA_ROOT+'\\'+f'{message}'+'\\'+f'{file_image}'
                os.remove(path_to_delete)

        return super().form_valid(form)

@user_passes_test(lambda u: u.is_superuser)
def sent_email_users(request , username , szkolenie , message):
    message = message
    emails = []
    szkolenie = str(szkolenie)
    username =str(username)
    
    if request.method == "POST":
        for i in Panel.objects.all():
            b=f'check{i.pk}'
            x= request.POST.get(b)
            if x == "on" :
                User=Panel.objects.get(pk=i.pk).email_user
                emails.append(User)
                if szkolenie == "bez":
                    szkolenie_id = User=Panel.objects.get(pk=i.pk).NewTraining
                    szkolenie = Szkolenie.objects.get(NewTraining=szkolenie_id).NewTraining

    send_message_user(message,emails,szkolenie)

    return redirect("ListaSzkolenUsersView",username=username,szkolenie=szkolenie) 
    
        