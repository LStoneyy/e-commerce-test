from django.contrib import admin
from .models import Product, Order, OrderItem, CartItem, Category, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "created_at"]
    list_filter = ["category", "created_at"]
    search_fields = ["name", "description"]
    list_editable = ["price", "stock"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total_price", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "id"]
    readonly_fields = ["created_at"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "price"]
    list_filter = ["order__created_at"]
    search_fields = ["product__name", "order__id"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]
    search_fields = ["user__username", "product__name"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "full_name", "city", "phone"]
    search_fields = ["user__username", "first_name", "last_name", "city"]
    list_filter = ["country", "city"]
