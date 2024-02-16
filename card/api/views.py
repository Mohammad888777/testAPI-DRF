from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from ..models import Cart,CartItem
from account.models import User
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from account.mixins import UserNotBeBlocked,UserNotBeBlockedForEver,NotBeingLoggedIn
from account.api.authentications import CombineAuthentication
from account.api.permissions import CustomLoginPermission
from category.models import Category




class AddCart(
    UserNotBeBlocked,
    UserNotBeBlockedForEver,
    APIView
):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]

    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            user=request.user
            cat=get_object_or_404(Category,
                                  id=self.kwargs.get("id"),
                                  is_active=True,
                                  parent__isnull=False,
                                  category_type="0"

                                  )
            user_cart=get_object_or_404(Cart,cart_id_custom=str(user.id))
            cart_items=None
            try:
                cart_items=CartItem.objects.get(user=user,category=cat,cart=user_cart,is_paid=False)
            except CartItem.DoesNotExist:
                cart_items=None
            
            if cart_items:
                cart_items.quantity+=1
                cart_items.save()
                return Response({
                    "quantity":cart_items.quantity,
                    "final":CartItem.objects.make_card(user=user)
                    })
            else:
                new_cart=CartItem.objects.create(
                    user=user,cart=user_cart,
                    category=cat,
                    quantity=1,is_paid=False
                )

                return Response({
                    "new":True,
                    "quantity":1,
                    "final":CartItem.objects.filter(user=user,is_paid=False).aggregate(s=Sum("category__price")).get("s",0)

                })


class IncreateCartItem(
    UserNotBeBlocked,UserNotBeBlockedForEver,APIView
):
    
    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            user=request.user
            cat=get_object_or_404(Category,
                                  id=self.kwargs.get("id"),
                                  is_active=True,
                                  parent__isnull=False,
                                  category_type="0"

                                  )
            item=get_object_or_404(CartItem,
                                   id=self.kwargs.get("c_id"),
                                   user=user,
                                   category=cat,
                                   is_paid=False
                                   )
            item.quantity+=1
            item.save()
            return Response({
                "added":True,
                "quantity":item.quantity,
                "final":CartItem.objects.make_card(user=user)

            })
    
                
            




class DecreaseCartItem(
    UserNotBeBlocked,UserNotBeBlockedForEver,APIView
):
    
    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            user=request.user
            cat=get_object_or_404(Category,
                                  id=self.kwargs.get("id"),
                                  is_active=True,
                                  parent__isnull=False,
                                  category_type="0"
                                  )
            item=get_object_or_404(CartItem,
                                   id=self.kwargs.get("c_id"),
                                   user=user,
                                   category=cat,
                                   is_paid=False
                                   )
            if item.quantity==0:
                item.delete()
                return Response({
                    "delete":True,
                    "final":CartItem.objects.make_card(user=user)                    
                })
            else:

                item.quantity-=1
                item.save()
                return Response({
                    "reduced":True,
                    "quantity":item.quantity,
                    "final":CartItem.objects.filter(user=user,is_paid=False).aggregate(s=Sum("category__price")).get("s",0)
                })
    