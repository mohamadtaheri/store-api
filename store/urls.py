from django.urls import path

from . import apiviews

urlpatterns = (
    [
        path("v1/products", apiviews.ProductList.as_view()),
        path("v1/products/new", apiviews.ProductCreat.as_view()),
        path("v1/products/<int:id>", apiviews.ProductRetrieveUpdateDestroy.as_view()),
    ]
    + [
        path("v1/carts", apiviews.ShoppingCartList.as_view()),
        path("v1/carts/new", apiviews.ShoppingCartCreat.as_view()),
        path(
            "v1/carts/<int:id>/update",
            apiviews.ShoppingCartUpdateView.as_view(),
        ),
    ]
    
)
