from django.urls import path

from . import apiviews

urlpatterns = [
    path("v1/cart_items", apiviews.CartItemList.as_view()),
    path("v1/products", apiviews.ProductList.as_view()),
    path("v1/products/new", apiviews.ProductCreat.as_view()),
    path("v1/products/<int:id>",apiviews.ProductRetrieveUpdateDestroy.as_view()),
] + \
[
    path("v1/shopping_carts",apiviews.ShoppingCartList.as_view()),
    path("v1/shopping_carts/new",apiviews.ShoppingCartCreat.as_view()),
    path("v1/shopping_carts/<int:id>",apiviews.ShoppingCartRetrieveUpdateDestroy.as_view()),
] + \
[
    path('v1/cart_items', apiviews.CartItemList.as_view()),
    path('v1/cart_items/new', apiviews.CartItemCreate.as_view()),
    path('v1/cart_items/<int:id>', apiviews.CartItemRetrieveUpdateDestroy.as_view()),
]
