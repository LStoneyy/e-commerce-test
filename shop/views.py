from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .cart import Cart

def home(request):
    return render(request, "shop/home.html")

def products(request):
    products = Product.objects.all()
    return render(request, "shop/products.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/product_detail.html", {"product": product})

def cart(request):
    cart = Cart(request)
    return render(request, "shop/cart.html", {"cart": cart})

# call cart class functions
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.add(product=product, quantity=1)
    return redirect("products")

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect("cart")

def update_cart(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get("quantity", 1))

    if quantity > 0:
        cart.update(product_id, quantity)
    else:
        cart.remove(product_id)
    
    return redirect("cart")