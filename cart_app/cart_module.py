from product_app.models import Product

CART_SESSION_ID = 'cart'
class Cart:
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(id=int(item['id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * int(item['price'])
            yield item


    def save(self):
        self.session.modified = True

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'id': product.id
            }
        self.cart[product_id]['quantity'] += int(quantity)
        self.save()

    def delete(self, id):
        id = str(id)
        if id in self.cart:
            del self.cart[id]
            self.save()

    def total(self):
        cart = self.cart.values()
        total = 0
        for i in cart:
            total += int(i['price']) * int(i['quantity'])
        return total

    def remove_cart(self):
        del self.session[CART_SESSION_ID]

