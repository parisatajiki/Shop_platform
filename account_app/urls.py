from django.urls import path
from . import views


# /account/
app_name = 'account_app'
urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('checkemail', views.CheckEmailView.as_view(), name='check_email'),

]