from django import forms
from django.core import validators
from .models import User
from django.contrib.auth.forms import UserCreationForm


def validate_phone(value):
    if value[0] != '0':
        raise forms.ValidationError(".شماره تلفن همراه باید با 0 شروع شود")


class LoginForm(forms.Form):
    username = forms.CharField( label='inter your username',widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(label='inter your pass', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Email already registered. please enter another email")



class CheckEmailForm(forms.Form):
    code = forms.CharField(validators=[validators.MaxLengthValidator(4)])
    username = forms.CharField(label='Enter your username',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Enter your password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm your password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='Enter your fullname',widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "dont mach")


        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            self.add_error('username', "Username already registered. please enter another username")