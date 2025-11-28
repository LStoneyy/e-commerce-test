from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .cart import Cart
from .models import CartItem

@receiver(user_logged_in)
def merge_cart_on_login(sender, user, request, **kwargs):
    cart = Cart(request)

    for item in cart:
        CartItem.objects.update_or_create(
            user=user,
            product=item["product"],
            defaults={"quantity": item["quantity"]},
        )

    # Warenkorb leeren
    cart.clear()
