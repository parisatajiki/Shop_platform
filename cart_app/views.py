from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import DiscountCodeForm
from product_app.models import Product
from .cart_module import Cart
from .models import Order, OrderItem, DiscountCode

from django.http import HttpResponse
from django.conf import settings
import requests
import json


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart_app/cart_details.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        quantity = request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product, quantity)
        return redirect('cart_app:cart')


class CartDelete(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart_app:cart')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],
                                     price=item['price'])
        cart.remove_cart()
        order = get_object_or_404(Order, id=pk)
        return redirect('cart_app:request_payment', order.id)


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect('cart_app:cart')

    def post(self, request):
        cart = Cart(request)
        address = request.POST.get("address")

        order = Order.objects.create(
            user=request.user,
            total_price=cart.total(),
            address=address
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

        cart.remove_cart()
        return redirect('cart_app:order_detail', pk=order.pk)


# class ApplyDiscountView(LoginRequiredMixin,View):
#     def post(self,request,pk):
#         form = DiscountCodeForm(request.POST)
#         order = get_object_or_404(Order,id=pk)
#         code = request.POST.get("name")
#         discount_code = get_object_or_404(DiscountCode , name=code)
#         if discount_code.quantity != 0:
#             order.total_price -= order.total_price * discount_code.discount/100
#             order.save()
#             discount_code.quantity -= 1
#             discount_code.save()
#         else:
#             form.add_error("name", "کد تخفیف منقضی شده است")
#         return render(request, 'cart_app/order_detail.html', {'form': form, 'order': order})


# Zarinpal

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'payment'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"

description = "نهایی کردن خرید شما از سایت ما"  # it's only an example

price = 100000  # it's only an example
CallbackURL = 'http://localhost:8000/verify/'  # you should customize it
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/cart/verify/'


def request_payment(request, pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    address = order.address
    order.address = f"{address} - {order.user.email}"
    order.save()
    request.session['order_id'] = str(order.id)

    data = {
        "merchant_id": settings.MERCHANT,
        "amount": order.total_price,
        "description": description,
        "callback_url": CallbackURL,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
        if response["data"]["code"] == 100:
            authority = response["data"]["authority"]
            order.authority = authority
            order.save()
            return redirect(f"{ZP_API_STARTPAY}{authority}")
        else:
            return {'status': False, 'code': str(response['Status'])}
        return response
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


class VerifyView(View):
    def get(self, request):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=int(order_id))

        status = request.GET.get('Status')
        authority = request.GET.get('Authority')

        if status != "OK":
            return HttpResponse("پرداخت توسط کاربر لغو شد یا ناموفق بود.")

        data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.total_price,
            "authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response["data"]["code"] == 100:
                order.is_paid = True
                order.save()
                return HttpResponse(f"پرداخت موفق بود. کد پیگیری: {response['data']['ref_id']}")
            else:
                return HttpResponse(f"پرداخت ناموفق بود. کد خطا: {response['data']['code']}")
        else:
            return HttpResponse("خطا در ارتباط با درگاه پرداخت.")
