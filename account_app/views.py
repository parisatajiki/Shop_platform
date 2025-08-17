from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect ,reverse
from django.views import View
from .forms import LoginForm, RegisterForm, CheckEmailForm
from .models import User, PendingUser

from django.core.mail import send_mail
from django.conf import settings

from random import randint


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "account_app/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect("home_app:home")
            else:
                form.add_error("username", '.نام کاربری و یا رمز شما اشتباه است')
        else:
            form.add_error("username", '.نام کاربری و یا رمز شما اشتباه است')

        return render(request, "account_app/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home_app:home")


class UserRegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "account_app/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = str(randint(1000, 9999))
            email = cd['email']
            send_mail(
                "کد تاییدیه",
                f"کد ورود به سایت فروشگاهی پریسا: {randcode}",
                "tajikiparisa535@gmail.com",
                [email],
                fail_silently=False,
            )
            print(randcode)
            PendingUser.objects.create(email=cd['email'], code=randcode)
            return redirect(reverse("account_app:check_email") + f"?email={cd['email']}")
        else:
            form.add_error("email","invalid data")

        return render(request, "account_app/register.html", {"form": form})


class CheckEmailView(View):
    def get(self, request):
        form = CheckEmailForm()
        return render(request, "account_app/check_email.html", {"form": form})

    def post(self, request):
        email = request.GET.get('email')
        form = CheckEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if PendingUser.objects.filter(code=cd['code'],email=email).exists():
                user,is_created = User.objects.get_or_create(email=email,username=cd['username'],full_name=cd['full_name'],password=cd['password1'])
                #is_created یک بولین هست که میتوانستیم برای نشان دادن خطاها ازش استفاده کنیم
                login(request, user)
                PendingUser.objects.filter(email=email).delete()
                return redirect("home_app:home")
        else:
            form.add_error("code", "invalid data")

        return render(request, "account_app/check_email.html", {"form": form})