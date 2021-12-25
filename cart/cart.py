from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("skey")

        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        self.cart = cart

    def add(self, product, qty):
        product_id = str(product.id)

        if product_id in self.cart:
            # self.cart[product_id]["qty"] = qty
            return False
        else:
            self.cart[product_id] = {"price": str(
                product.regular_price), "qty": qty}

        self.save()
        return True

    def update(self, product, qty):
        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id]["qty"] = qty
        self.save()

    def delete(self, product_id):
        str_product_id = str(product_id)

        if str_product_id in self.cart:
            del self.cart[str_product_id]
            self.save()

    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())

    def __iter__(self):
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def clear(self):
        # Remove basket from session
        del self.session['skey']
        self.save()

    def save(self):
        self.session.modified = True
