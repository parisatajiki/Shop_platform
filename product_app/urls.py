from django.urls import path
from .views import CategoryProduct,ProductDetail



# /products
app_name = 'product_app'
urlpatterns = [
    path('<slug:slug>/', CategoryProduct.as_view(), name='category_products'),
    path('', CategoryProduct.as_view(), name='all_products'),
    path('detail/<slug:slug>',ProductDetail.as_view(), name='product_detail'),
]
