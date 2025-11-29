from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem, Order, OrderItem
from .cart import Cart
from django.contrib import messages
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction


def home(request):
    featured_products = Product.objects.filter(stock__gt=0)[:6]
    return render(request, "shop/home.html", {"featured_products": featured_products})


def products(request):
    products = Product.objects.all()

    # Sortierung
    sort = request.GET.get("sort", "name")
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-created_at")
    else:
        products = products.order_by("name")

    return render(
        request, "shop/products.html", {"products": products, "current_sort": sort}
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/product_detail.html", {"product": product})


def cart_view(request):
    cart = Cart(request)
    return render(request, "shop/cart.html", {"cart": cart})


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, f"{product.name} ist leider ausverkauft.")
        return redirect("product_detail", pk=product_id)

    cart.add(product=product, quantity=1)
    messages.success(request, f"{product.name} wurde zum Warenkorb hinzugefügt")
    return redirect(request.META.get("HTTP_REFERER", "products"))


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.success(request, "Produkt wurde entfernt")
    return redirect("cart")


def update_cart(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get("quantity", 1))

    if quantity > 0:
        product = get_object_or_404(Product, id=product_id)
        if quantity > product.stock:
            messages.error(request, f"Nur {product.stock} Stück verfügbar")
            return redirect("cart")
        cart.update(product_id, quantity)
    else:
        cart.remove(product_id)

    return redirect("cart")


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, "Ihr Warenkorb ist leer")
        return redirect("products")

    if request.method == "POST":
        try:
            with transaction.atomic():
                # Order erstellen
                order = Order.objects.create(
                    user=request.user,
                    total_price=cart.get_total_price(),
                    status="pending",
                )

                # OrderItems erstellen und Stock reduzieren
                for item in cart:
                    product = item["product"]
                    quantity = item["quantity"]

                    # Stock prüfen
                    if product.stock < quantity:
                        raise ValueError(
                            f"{product.name} ist nicht mehr in ausreichender Menge verfügbar"
                        )

                    # OrderItem erstellen
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=item["price"],
                    )

                    # Stock reduzieren
                    product.stock -= quantity
                    product.save()

                # Warenkorb leeren
                if request.user.is_authenticated:
                    CartItem.objects.filter(user=request.user).delete()
                cart.clear()

                messages.success(
                    request, f"Bestellung #{order.id} wurde erfolgreich aufgegeben!"
                )
                return redirect("order_detail", order_id=order.id)

        except ValueError as e:
            messages.error(request, str(e))
            return redirect("cart")
        except Exception as e:
            messages.error(
                request, "Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut."
            )
            return redirect("cart")

    return render(request, "shop/checkout.html", {"cart": cart})


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "shop/orders.html", {"orders": user_orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "shop/order_detail.html", {"order": order})


@login_required
def profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        user = request.user
        user.username = username
        user.email = email
        user.save()

        messages.success(request, "Profil erfolgreich aktualisiert")
        return redirect("profile")

    return render(request, "shop/profile.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Konto wurde erstellt und Sie sind jetzt eingeloggt!"
            )
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/registration.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Session-Cart übertragen
            cart = Cart(request)
            cart.merge_guest_cart()

            messages.success(request, "Erfolgreich eingeloggt!")
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Sie wurden erfolgreich ausgeloggt")
    return redirect("home")
