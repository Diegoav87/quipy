from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name="cart"),
    path("cart-add/", views.cart_add, name="cart_add"),
    path("cart-delete/", views.cart_delete, name="cart_delete"),
    path("cart-update/", views.cart_update, name="cart_update")
]
