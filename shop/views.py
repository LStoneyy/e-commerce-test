from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem
from .cart import Cart
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

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
    messages.success(
        request,
        f"{product.name} wurde zum Warenkorb hinzugefügt"
        )
    return redirect("products")

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.success(
        request,
        "Produkt wurde zum entfernt"
        )
    return redirect("cart")

def update_cart(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get("quantity", 1))

    if quantity > 0:
        cart.update(product_id, quantity)
    else:
        cart.remove(product_id)
    
    return redirect("cart")

def merge_cart(request):
    if not request.user.is_authenticated:
        return

    cart = Cart(request)

    for item in cart:
        CartItem.objects.update_or_create(
            user=request.user,
            product=item["product"],
            defaults={"quantity": item["quantity"]},
        )
    
    # für leere session
    cart.clear()


# User forms/views
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Konto wurde erstellt!"
                )
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/registration.html", {"form": form})