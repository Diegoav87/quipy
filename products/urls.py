from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.all_products, name="all_products"),
    path('shop/', views.shop, name="shop"),
    path('product/<slug:slug>/', views.product_detail, name="product_detail"),
    path('search/<slug:slug>/', views.get_by_category, name="category")
]
