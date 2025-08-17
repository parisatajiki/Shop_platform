from django.shortcuts import render
from django.views.generic import TemplateView
from product_app.models import Product

class HomeView(TemplateView):
    template_name = 'home_app/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


