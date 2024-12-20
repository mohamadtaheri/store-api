from rest_framework import serializers
from .models import Product, ShoppingCartItem, ShoppingCart


class ShoppingCartSerializer(serializers.ModelSerializer):
    subtotal = serializers.FloatField(read_only=True)
    total = serializers.FloatField(read_only=True)
    taxes = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ShoppingCart
        fields = (
            "id",
            "name",
            "address",
            'subtotal',
            'total',
            'taxes',
        )


class CartItemSerializer(serializers.ModelSerializer):
    shopping_cart_data = serializers.SerializerMethodField()
    total = serializers.FloatField(read_only=True)
    class Meta:
        model = ShoppingCartItem
        fields = (
            "shopping_cart",
            'shopping_cart_data',
            "product",
            "quantity",
            'total',
        )

    def get_shopping_cart_data(self, instance):
        item = ShoppingCart.objects.filter(id=instance.shopping_cart.id)
        return ShoppingCartSerializer(item, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(label="Desc", min_length=2, max_length=100)
    card_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "sale_start",
            "sale_end",
            "is_on_sale",
            "current_price",
            "card_items",
        )

    def get_card_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data

 
    
