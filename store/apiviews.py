from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.validators import ValidationError

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from .serializers import ProductSerializer, ShoppingCartSerializer, CartItemSerializer
from .models import Product, ShoppingCart, ShoppingCartItem


class ProductPagination(LimitOffsetPagination):
    max_limit = 100
    default_limit = 10


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_fields = ("id",)
    search_fields = (
        "name",
        "description",
    )
    pagination_class = ProductPagination

    def get_queryset(self):

        params_dict = self.request.query_params.dict()

        if "onsale" in params_dict.keys():
            onsale = params_dict["onsale"]
            queryset = Product.objects.all()
            from django.utils import timezone

            now = timezone.now()
            if onsale.lower() == "true":
                return queryset.filter(sale_start__lte=now, sale_end__gte=now)
            else:
                from django.db.models import Q

                return queryset.filter(Q(sale_end__lte=now) | Q(sale_end__isnull=True))

        return super().get_queryset()


class ProductCreat(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get("price")
            if price is not None and float(price) <= 0.0:
                raise ValidationError({"price": "Price must be above 0.0$!"})
        except ValueError:
            raise ValidationError({"price": "Price must be a number!"})

        return super().create(request, *args, **kwargs)


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get("id")
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache

            cache.delete(f"product_data_{product_id}")
        return response

    def update(self, request, *args, **kwargs):

        try:
            price = request.data.get("price")
            if price is not None and float(price) <= 0.0:
                raise ValidationError({"price": "Price must be above 0.0$!"})
        except ValueError:
            raise ValidationError({"price": "Price must be a number!"})

        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            product = response.data
            product_set = {
                "name": product["name"],
                "description": product["description"],
                "price": product["price"],
            }
            from django.core.cache import cache

            cache.set(f"product_data_{product['id']}", product_set)
        return response


class ShoppingCartList(ListAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    
class ShoppingCartCreat(CreateAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    
class ShoppingCartRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    lookup_field = 'id'
    
    def delete(self, request, *args, **kwargs):
        id = request.data.get('id')
        response =  super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete(f'shoppoindcard_data_{id}')
        return response
    
    def update(self, request, *args, **kwargs):
        response =  super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            card_set = {
                "name": request.data['name'],
                "address" : request.data['address']
            }
            cache.set(f'shoppoindcard_data_{request.data.get('id')}', card_set)
        return response
    
    
class CartItemList(ListAPIView):
    queryset = ShoppingCartItem.objects.all()
    serializer_class = CartItemSerializer
    
class CartItemCreate(CreateAPIView):
    queryset = ShoppingCartItem.objects.all()
    serializer_class = CartItemSerializer
    
class CartItemRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    lookup_field = 'id'