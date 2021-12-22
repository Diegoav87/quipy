from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.


def categories(request):
    return {
        "categories": Category.objects.all()
    }


def all_products(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def get_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category.html', {'products': products, "category": category})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, "products/product_detail.html", {"product": product})
