from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView
from .models import Product, Category



class CategoryProduct(View):
    def get(self, request,slug=None):
        if slug:
            category = get_object_or_404(Category, slug=slug)
            products = Product.objects.filter(category=category)
        else:
            products = Product.objects.all()
        return render(request,'product_app/products.html',{'products':products})




class ProductDetail(DetailView):
    model = Product
    template_name = 'product_app/product_details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, slug=self.kwargs['slug'])
        return context





