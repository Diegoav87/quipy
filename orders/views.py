from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from cart.cart import Cart
from .models import Order, OrderItem

# Create your views here.


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == "POST":
        order_key = request.POST.get("order_key")
        cart_total = cart.get_subtotal_price()

        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user=request.user,
                full_name="name",
                address1="add1",
                address2="add2",
                total_paid=cart_total,
                order_key=order_key,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item["product"], price=item["price"], quantity=item["qty"]
                )

            return JsonResponse({"success": "something"})
        return JsonResponse({"error": "Order already exists"}, status=400)


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)
