from rest_framework import serializers
from ..models import Order,FreeOrderProduct,OrderProduct
from card.api.serializers import CartItemSerializer
from django.core.validators import validate_email as emailValdation


class OrderSerializer(serializers.ModelSerializer):
    carts=CartItemSerializer(many=True,required=False)

    pay_link=serializers.SerializerMethodField(method_name="url_pay")

    def url_pay(self,obj:Order):
        return f'http://127.0.0.1:8000/order/gateway/{obj.id}'

    
    class Meta:
        model=Order
        fields=[
            'id',
            'name',
            'last_name',
            'email',
            # 'pay_linl',
            'pay_link',
            'user',
            'carts',
            'order_custom_id',
            'order_total',
            'tax',
            'total_after_use_copon',
            'used_copon',
            'status',
            'is_ordered',
            'created',
        ]

        extra_kwargs={
            'id':{"read_only":True},
            'pay_link':{"read_only":True,'allow_null':True},
            'user':{"read_only":True},
            'carts':{"read_only":True},
            'order_custom_id':{"read_only":True},
            'order_total':{"read_only":True},
            'tax':{"read_only":True},
            'total_after_use_copon':{"read_only":True},
            'used_copon':{"read_only":True},
            'status':{"read_only":True},
            'is_ordered':{"read_only":True},
            'created':{"read_only":True},
            'name':{"required":True},
            'last_name':{"required":True},
            'email':{"required":True},
        }

    
    def validate_email(self,value):
        try:
            emailValdation(value)
        except Exception as e:
            raise serializers.ValidationError(e)
        return value
    
    def validate_name(self,value):
        if len(value)<3:
            raise serializers.ValidationError("min lenght error")
        return value
    
    def create(self, validated_data:dict):
        new_o=Order(
            name=validated_data.get("name"),
            last_name=validated_data.get("last_name"),
            email=validated_data.get("email")
        )
        new_o.save()
        return new_o
    








class OrderPSerializer(serializers.ModelSerializer):
    cat_image=serializers.ImageField(source="category.image")
    name=serializers.CharField(source="category.name")
    class Meta:
        model=OrderProduct
        fields=[
            'id',
            'cat_image',
            'name',

        ]




class FreeOpSerilaiazaer(serializers.ModelSerializer):
    free_cat_image=serializers.ImageField(source="free_category.image")
    name=serializers.CharField(source="free_category.name")

    class Meta:
        model=FreeOrderProduct
        fields=[
            'id',
            'free_cat_image',
            'name'

        ]