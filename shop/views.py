from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    return render(request, "shop/home.html")

def products(request):
    products = Product.objects.all()
    return render(request, "shop/products.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/product_detail.html", {"product": product})