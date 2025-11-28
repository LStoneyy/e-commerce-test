"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products, name="products"),
    path("products/product/<int:pk>/", views.product_detail, name="product_detail"),
    path("cart/", views.home, name="cart"),
    path("cart/add/<int:product_id>/", views.home, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.home, name="remove_from_cart"),
    path("cart/update/<int:product_id>/", views.home, name="update_cart"),
]
