from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("order-placed/", views.order_placed, name="order_placed"),
    path("webhook/", views.stripe_webhook)
]
