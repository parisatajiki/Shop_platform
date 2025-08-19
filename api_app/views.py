from django.shortcuts import get_object_or_404

from account_app.models import User
from product_app.models import Product
from cart_app.models import Order, OrderItem
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from . serializer import AccountSerializer,ProductSerializer,OrderSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser

class UserRegister(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username'].lower()
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            user = User.objects.create_user(username=username, password=password,email=email)
            user.save()
            return Response({"response": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#CRUD
class ProductsModelView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]


class Orders(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# class OrderDetail(APIView):
#     def get(self, request, pk=None):
#         order = get_object_or_404(Order, user=request.user, id=pk)
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)
#
#     def post(self, request, pk=None):
#         order = get_object_or_404(Order, user=request.user, id=pk)
#         is_paid = request.data.get("is_paid")
#         if is_paid is not None:
#             order.is_paid = bool(is_paid)
#             order.save()
#         return Response({"message": "Order updated"}, status=status.HTTP_200_OK)




class OrderDetail(APIView):
    def get(self, request, pk=None):
        order = get_object_or_404(Order, user=request.user, id=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request, pk=None):
        order = get_object_or_404(Order, user=request.user, id=pk)

        action = request.data.get("action")   # add / remove / update/pay
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if action == "add":
            product = get_object_or_404(Product, id=product_id)
            item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={'price': product.price, 'quantity': quantity}
            )
            if not created:
                item.quantity += quantity
                item.save()

        elif action == "remove":
            item = get_object_or_404(OrderItem, order=order, product_id=product_id)
            item.delete()

        elif action == "update":
            item = get_object_or_404(OrderItem, order=order, product_id=product_id)
            item.quantity = quantity
            item.save()

        elif action == "pay":
            order.is_paid = True
            order.save()

        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        order.total_price = sum(item.price * item.quantity for item in order.items.all())
        order.save()

        order.refresh_from_db()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)























