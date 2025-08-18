from django.db import models
from account_app.models import User
from product_app.models import Product



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    address = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "اطلاعات خرید کاربر"
        verbose_name_plural = "اطلاعات خرید کاربرها"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.SmallIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.title} {self.quantity} {self.price}'

    class Meta:
        verbose_name = "اطلاعات خرید محصول"
        verbose_name_plural = "اطلاعات خرید محصول ها"


class DiscountCode(models.Model):
    name = models.CharField(max_length=20 , unique=True)
    discount = models.SmallIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name