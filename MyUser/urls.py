from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/',views.login_view,name='login_view'),
    path('logout/',views.logout_view,name='logout_view'),
    path('register/',views.register, name='register'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="password_reset.html",email_template_name="password_reset_email.html"), name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path("password_reset_confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view( template_name="password_reset_complete.html"), name="password_reset_complete"),
    path('register/num/<str:user>/',views.registerNum_view, name='registerNum')
]