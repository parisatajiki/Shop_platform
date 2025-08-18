from django.shortcuts import render
from django.views.generic import TemplateView,View
from product_app.models import Product
from django.core.mail import send_mail


class HomeView(TemplateView):
    template_name = 'home_app/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class AboutView(TemplateView):
    template_name = 'home_app/about.html'


class ContactView(View):
    def get(self, request):
        return render(request, 'home_app/contact.html')
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        send_mail(
            "contact message",
            f"Here is the message:\nfrom name:{name} and email:{email}\nmessage:{message}",
            "tajikiparisa535@gmail.com",
            ["parisatajiki7547@gmail.com"],
            fail_silently=False,
        )
        return render(request, 'home_app/index.html')

