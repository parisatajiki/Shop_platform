from product_app.models import Category, Product

def product_context(request):
    categories = Category.objects.all()
    return {'categories': categories}