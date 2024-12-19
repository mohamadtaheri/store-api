from django.contrib import admin

# Register your models here.
from .models import Product,ShoppingCart,ShoppingCartItem

admin.site.register(Product)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
