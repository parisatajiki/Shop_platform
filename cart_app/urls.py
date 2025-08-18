from django.urls import path
from . import views

# /cart
app_name = 'cart_app'
urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/<int:pk>', views.CartAddView.as_view(), name='cart_add'),
    path('delete/<str:id>', views.CartDelete.as_view(), name='cart_delete'),
    path('order/create/', views.CreateOrderView.as_view(), name='create_order'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    # path('applydiscount/<int:pk>', views.ApplyDiscountView.as_view(), name='apply_discount'),
    path('request/<int:pk>', views.request_payment, name='request_payment'),
    path('verify/', views.VerifyView.as_view(), name='verify_payment'),
    # path('sendrequest/<int:pk>', views.SendRequestView.as_view(), name='send_request'),
]
