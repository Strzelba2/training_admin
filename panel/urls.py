from django.urls import path
from .views import (PanelListView , formularz,correct_form , email,ListaSzkolenView , delete_Szkolenie,Create_szkolenie_view,update_szkolenie_view,ListaUserView,
                    update_Users_view,Create_User_view,delete_User,ListaSzkolenUsersView,delete_Userszkolenie,update_szkolenie_users,convert_to_CSV,sent_email_users,
                    MessageList,delete_Message,Create_Message,update_Message_email,archiwum_Szkolenie,)


urlpatterns = [
    path('list/<str:username>/', PanelListView.as_view(), name='Panel'), 
    path('formularz/', formularz.as_view(), name='formularz'), 
    path('corectForm/<str:email>/<str:name>/', correct_form, name='corectForm'), 
    path('email/', email, name='email'),
    path('list/<str:username>/message/', MessageList.as_view(), name='MessageList'),
    path('list/<str:username>/message/delete/', delete_Message, name='delete_Message'),
    path('list/<str:username>/message/create/', Create_Message.as_view(), name='Create_Message'),
    path('list/<str:username>/message/<int:pk>/update/', update_Message_email.as_view(), name='update_Message_email'),
    path('list/<str:username>/szkolenia/<str:szkolenie>/', ListaSzkolenView.as_view(), name='ListaSzkolenView'),
    path('list/<str:username>/szkolenia/<str:szkolenie>/delete/', delete_Szkolenie, name='delete_szkolenie_view'),
    path('list/<str:username>/szkolenia/<str:szkolenie>/archiwum/', archiwum_Szkolenie , name='archiwum_Szkolenie'),
    path('list/<str:username>/szkolenia/<str:szkolenie>/create/', Create_szkolenie_view.as_view(), name='Create_szkolenie_view'),
    path('list/<str:username>/szkolenia/<str:szkolenie>/<int:pk>/update/', update_szkolenie_view.as_view(), name='update_szkolenie_view'),
    path('list/<str:username>/users/', ListaUserView.as_view(), name='ListaUserView'),
    path('list/<str:username>/users/<int:pk>/update/', update_Users_view.as_view(), name='update_Users_view'),
    path('list/<str:username>/users/create/', Create_User_view.as_view(), name='Create_User_view'),
    path('list/<str:username>/users/delete/', delete_User, name='delete_User_view'),
    path('list/<str:username>/ListaSzkolenUsers/<str:szkolenie>/', ListaSzkolenUsersView.as_view(), name='ListaSzkolenUsersView'),
    path('list/<str:username>/ListaSzkolenUsers/<str:szkolenie>/delete/', delete_Userszkolenie, name='delete_Userszkolenie'),
    path('list/<str:username>/ListaSzkolenUsers/<str:szkolenie>/<int:pk>/update/', update_szkolenie_users.as_view(), name='update_szkolenie_users'),
    path('list/<str:username>/ListaSzkolenUsers/<str:szkolenie>/CSV/', convert_to_CSV, name='convert_to_CSV'),
    path('list/<str:username>/ListaSzkolenUsers/<str:szkolenie>/<str:message>/sent_email/', sent_email_users, name='sent_email_users')
    ,
    
]