from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .cart import Cart
from products.models import Product

# Create your views here.


def cart(request):
    return render(request, 'cart/cart.html')


def cart_add(request):
    cart = Cart(request)

    if request.method == "POST":
        try:
            product_id = int(request.POST.get("productId"))
            product_qty = int(request.POST.get("productQty"))
        except:
            return JsonResponse({"error": "Something went wrong"}, status=500)
        product = get_object_or_404(Product, id=product_id)
        added = cart.add(product=product, qty=product_qty)

        if added == False:
            return JsonResponse({"error": "Item is already in cart"}, status=400)

        cart_qty = cart.__len__()
        return JsonResponse({"qty": cart_qty})


def cart_update(request):
    cart = Cart(request)
    if request.method == "POST":
        try:
            product_id = int(request.POST.get("productId"))
            product_qty = int(request.POST.get("productQty"))
        except:
            return JsonResponse({"error": "Something went wrong"}, status=500)
        cart.update(product=product_id, qty=product_qty)

        cart_qty = cart.__len__()
        cart_subtotal = cart.get_subtotal_price()
        return JsonResponse({"qty": cart_qty, "subtotal": cart_subtotal})


def cart_delete(request):
    cart = Cart(request)

    if request.method == "POST":
        try:
            product_id = int(request.POST.get("productId"))
        except:
            return JsonResponse({"error": "Something went wrong"}, status=500)
        cart.delete(product_id=product_id)

        cart_qty = cart.__len__()
        cart_subtotal = cart.get_subtotal_price()
        return JsonResponse({"qty": cart_qty, "subtotal": cart_subtotal})
