from decimal import Decimal
from .models import Product, CartItem
from django.contrib.auth.models import User

# Session management für cart + helper functions

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user

        # session cart for guests
        self.session_cart = self.session.get("cart", {})
    
    def add(self, product, quantity=1):
        if self.user.is_authenticated:
            item, created = CartItem.objects.get_or_create(
                user=self.user,
                product=product,
                defaults={"quantity": 0},
            )

            item.quantity += quantity
            item.save()
        else:
            product_id = str(product.id)
            if product_id not in self.session_cart:
                self.session_cart[product_id] = {"quantity": 0, "price": str(product.price)}
            self.session_cart[product_id]["quantity"] += quantity
            self.save()

    def remove(self, product_id):
        if self.user.is_authenticated:
            CartItem.objects.filter(
                user=self.user,
                product_id=product_id,
            ).delete()
        else:
            product_id = str(product_id)
            if product_id in self.session_cart:
                del self.session_cart[product_id]
                self.save()
    
    def update(self, product_id, quantity):
        if self.user.is_authenticated:
            CartItem.objects.filter(
                user=self.user,
                product_id=product_id
            ).update(quantity=quantity)
        else:
            product_id = str(product_id)
            if product_id in self.session_cart:
                self.session_cart[product_id]["quantity"] = quantity
                self.save()
    
    def save(self):
        self.session["cart"] = self.session_cart
        self.session.modified = True

    def clear(self):
        # only clear session cart!
        if "cart" in self.session:
            del self.session["cart"]
        self.save()

    def get_total_price(self):
        return sum(item["total_price"] for item in self)
    
    def __iter__(self):
        if self.user.is_authenticated:
            items = CartItem.objects.filter(user=self.user).select_related("product")

            for item in items:
                yield {
                    "product": item.product,
                    "price": item.product.price,
                    "quantity": item.quantity,
                    "total_price": item.product.price * item.quantity,
                }
        else:
            product_ids = self.session_cart.keys()
            products = Product.objects.filter(id__in=product_ids)

            for product in products:
                data = self.session_cart[str(product.id)]
                price = Decimal(data["price"])
                quantity = data["quantity"]

                yield {
                    "product": product,
                    "price": price,
                    "quantity": quantity,
                    "total_price": price * quantity,
                }
            
        
    def __len__(self):
        if self.user.is_authenticated:
            return sum(item.quantity for item in CartItem.objects.filter(user=self.user))
        return sum(item["quantity"] for item in self.session_cart.values())