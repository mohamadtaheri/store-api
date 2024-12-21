from rest_framework import serializers
from .models import Product, ShoppingCartItem, ShoppingCart


class CartItemSerializer(serializers.ModelSerializer):
    total = serializers.FloatField(read_only=True)
    id = serializers.IntegerField(read_only=True, required=False)
    class Meta:
        model = ShoppingCartItem
        fields = (
            "id",
            "product",
            "quantity",
            "total",
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    subtotal = serializers.FloatField(read_only=True)
    total = serializers.FloatField(read_only=True)
    taxes = serializers.FloatField(read_only=True)
    items = CartItemSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = [
            "id",
            "name",
            "address",
            "items",
            "subtotal",
            "total",
            "taxes",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        shopping_cart = ShoppingCart.objects.create(**validated_data)

        # Create related ShoppingCartItems
        for item_data in items_data:
            ShoppingCartItem.objects.create(cart=shopping_cart, **item_data)

        return shopping_cart

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.save()

        # # Update the nested items
        items_data = validated_data.get("items", [])
        existing_items = {item.id: item for item in instance.items.all()}
        for item_data in items_data:
            item_id = item_data.get("id", None)
            if (item_id) and (item_id in existing_items):
                # Update existing ShoppingCartItem
                existing_item = existing_items.pop(item_id)
                existing_item.product = item_data.get("product", existing_item.product)
                existing_item.quantity = item_data.get(
                    "quantity", existing_item.quantity
                )
                existing_item.save()
            else:
                # Create a new ShoppingCartItem
                ShoppingCartItem.objects.create(cart=instance, **item_data)

        # Delete items not included in the request
        for remaining_item in existing_items.values():
            remaining_item.delete()

        return instance


class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(label="Desc", min_length=2, max_length=100)

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
        )


class ProductStatSerializer(serializers.Serializer):
    stats = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField())
    )
