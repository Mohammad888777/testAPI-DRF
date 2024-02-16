from rest_framework import serializers
from ..models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_price=serializers.FloatField(source="category.price")
    class Meta:
        model=CartItem
        fields=[
            'id',
            'quantity',
            'category',
            'user',
            'is_paid',
            'product_price'
        ]
        extra_kwargs={
            'id':{"read_only":True},
            'quantity':{"read_only":True},
            'category':{"read_only":True},
            'user':{"read_only":True},
            'is_paid':{"read_only":True},
            'product_price':{"read_only":True},
        }