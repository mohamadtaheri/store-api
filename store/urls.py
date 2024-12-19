from django.urls import path

from .apiviews import ProductList

urlpatterns = [
    path('v1/products', ProductList.as_view(), name='api.products')
]
