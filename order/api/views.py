from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializers import OrderSerializer,OrderPSerializer,FreeOpSerilaiazaer
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from account.mixins import  UserNotBeBlocked,UserNotBeBlockedForEver
from account.api.authentications import CombineAuthentication
from account.api.permissions import CustomLoginPermission
from ..models import Order,generate_order_id,FreeOrderProduct,OrderProduct
from django.db import transaction
from django.shortcuts import get_object_or_404
from card.models import CartItem
from account.models import User,MyProfile,Ticket,Message
from category.models import Category,Copon,SpecialCopon
from card.api.serializers import CartItemSerializer
from django.utils import timezone
from ..tasks import send_payment_request
from rest_framework.serializers import ValidationError
import requests
from account.api.serializers import ProfileSerializer,TicketCreateSerializer,MessageCreateSerializer
from category.paginatons import CustomPagination
from category.utils import hande_paginator
from category.api.serializers import CategoryFirstSerializer
from django.db.models import Q
from product.models import ProductFile,ProductVideo,ProductVoice
from product.api.serializers import FileProductSerializer,VoiceSerializer,VideoSerializer


class MakeOrder(APIView):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]

    def get(self,request,*args,**extra_kwargs):
        user=request.user
        u_carts=CartItem.objects.filter(
            user=user,is_paid=False
        ) 
        final_to_pay=CartItem.objects.make_card(user)
        f1=CartItemSerializer(instance=u_carts,many=True)
        
        return Response({
            'f1':f1.data,
            'final':final_to_pay
        })
    
    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            user=request.user
            data:dict=request.data
            copon=data.get("copon")
            final_to_pay=CartItem.objects.make_card(user)
            u_carts=CartItem.objects.filter(
            user=user,is_paid=False
        )

            if copon:
                now=timezone.now()
                
                c=get_object_or_404(Copon,copone_code=copon,
                                    is_active=True,number__gt=0,
                                    expire_time__gt=now
                                    )
                final=(c.off_percent*final_to_pay)/100
                new_ord=OrderSerializer(data=data)
                new_ord.is_valid(raise_exception=True)
                o=new_ord.save()
                o.user=user
                for i in u_carts:
                    o.carts.add(i)
                    o.save()
                o.order_custom_id=generate_order_id()
                o.order_total=final_to_pay
                o.total_after_use_copon=final
                o.tax=1000
                o.used_copon=True
                o.save()
                return Response(new_ord.data)



            else:

                new_ord=OrderSerializer(data=data)
                new_ord.is_valid(raise_exception=True)
                o=new_ord.save()
                o.user=user
                for i in u_carts:
                    o.carts.add(i)
                    o.save()
                o.order_custom_id=generate_order_id()
                o.order_total=final_to_pay
                o.total_after_use_copon=final_to_pay
                o.tax=1000
                o.used_copon=False
                o.save()
                return Response(new_ord.data)
            


class MyOrders(
    APIView
):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]

    def get(self,request,*args,**kwargs):

        user=request.user
        ors=Order.objects.filter(
            user=user,
            is_ordered=False,
            status="New"
        )
        s=OrderSerializer(instance=ors,many=True)
        return Response(s.data)
    




class MakeFreeOrder(
    APIView
):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]

    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            c=get_object_or_404(Category,
                                category_type="1",
                                is_active=True,
                                id=self.kwargs.get("id")
                                )
            new_or=FreeOrderProduct(
                free_category=c,
                user=request.user,
            )
            new_or.save()
            return Response({
                "new":True
            })




class MyProfileView(APIView):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]

    def get(self,request,*args,**kwargs):
        user=request.user
        p=get_object_or_404(MyProfile,user=user)
        s=ProfileSerializer(instance=p)
        return Response(s.data)
    
    def put(self,request,*args,**kwargs):
        user=request.user
        p=get_object_or_404(MyProfile,user=user)
        data:dict=request.data
        s=ProfileSerializer(instance=p,data=data,)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)
    



class MyAllCategoryeis(APIView):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]

    def get(self,request,*args,**kwargs):
        user=request.user
        page=self.request.GET.get("page",1)
        perPage=self.request.GET.get("perPage",1)
        o=OrderProduct.objects.filter(user=user)
        f=FreeOrderProduct.objects.filter(user=user)
        os=OrderPSerializer(instance=o,many=True)
        fs=FreeOpSerilaiazaer(instance=f,many=True)
        z=[]
        z.extend([os.data,fs.data])
        print(z)
        # h=hande_paginator(z,perPage=perPage,page=page)
        return Response(z)
    


class SavedCategory(APIView):

    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]  

    def get(self,request,*args,**kwargs):
        perPage=self.request.GET.get("perPage",1)
        page=self.request.GET.get("page",1)
        u=request.user.category_set.all()
        h=hande_paginator(u,perPage=perPage,page=page)
        s=CategoryFirstSerializer(instance=h,many=True,context={'request':request})
        return Response(s.data)
    



class CreateTicketView(
    APIView
):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication] 

    def post(self,request,*args,**kwargs):
        with transaction.atomic():

            user=request.user
            data:dict=request.data
            t=TicketCreateSerializer(data=data)
            t.is_valid(raise_exception=True)
            new_t=t.save()
            new_t.sender_user=user
            new_t.save()
            return Response(t.data)
        



class MyTicketsView(APIView):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication] 

    def get(self,request,*args,**kwargs):
        user:User=request.user
        print("$$$$$$$$$")
        print("$$$$$$$$$")
        # print(user.last_login)
        print("$$$$$$$$$")
        print("$$$$$$$$$")
        print("$$$$$$$$$")
        print("$$$$$$$$$")
        page=self.request.GET.get("page",1)
        perPage=self.request.GET.get("perPage",2)
        ticket_type=self.request.GET.get('type',None)
        # ticket_rec=self.request.GET.get("ticket_rec",None)



        ts=Ticket.objects.filter(sender_user=user).filter(
            Q(ticket_type=ticket_type) if ticket_type else Q()
        )
        pg_=hande_paginator(ts,perPage,page)

        ser=TicketCreateSerializer(instance=pg_,many=True)
        openend=Ticket.objects.opened_tickets(user)
        closed_tickets=Ticket.objects.closed_tickets(user)
        inspected_tickets=Ticket.objects.inspected_tickets(user)
        answered_tickets=Ticket.objects.answered_tickets(user)
        z=[]
        z.extend([
            ser.data,openend,
            closed_tickets,
            inspected_tickets,
            answered_tickets
        ])
        return Response(z)




class CreateMessageView(APIView):

    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication] 

    def post(self,request,*args,**kwargs):

        with transaction.atomic():
            user=request.user
            data:dict=request.data
            t=get_object_or_404(Ticket,
                                id=self.kwargs.get("id"),
                                sender_user=user
                                )
            
            new_msg=MessageCreateSerializer(data=data)
            new_msg.is_valid(raise_exception=True)
            m=new_msg.save()
            m.sender_messager=user
            m.ticket=t
            m.save()

            return Response(new_msg.data)
        
    


class PayProducts(
    APIView
):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication] 

    def get(self,request,*args,**kwargs):
        user=request.user
        c=get_object_or_404(
            Category,
            is_active=True,
            id=self.kwargs.get("id"),
            category_type="0"
        )
        c_ser=CategoryFirstSerializer(c)
        p=OrderProduct.objects.filter(
            category=c,
            order__isnull=False,
            payment__isnull=False,
            order__status="Completed",
            order__is_ordered=True,
            ordered=True,
            user=user
        )
        if not p.exists():
            raise ValidationError("you have not permission to access")
        v=ProductVideo.objects.filter(is_active=True,category=c)
        vo=ProductVoice.objects.filter(is_active=True,category=c)
        f=ProductFile.objects.filter(is_active=True,category=c)

        v_ser=VideoSerializer(v,many=True)
        vo_ser=VideoSerializer(vo,many=True)
        f_ser=VideoSerializer(f,many=True)

        final=[]
        final.extend([
            v_ser.data,vo_ser.data,f_ser.data,
            c_ser.data
        ])
        return Response(final)
    



class FreeProducts(
    APIView
):
    
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication] 

    def get(self,request,*args,**kwargs):
        user=request.user

        c=get_object_or_404(
            Category,
            id=self.kwargs.get("id"),
            category_type="1",
            is_active=True,
        )

        o=OrderProduct.objects.filter(
            user=user,
            category=c,
            payment_isnull=False,
            order__status="Completed",
            order__is_ordered=True,
            ordered=True,
        )
        if not o.exists():
            raise ValidationError("not allowed to access this category for this user ")
        
        v=ProductVideo.objects.filter(is_active=True,category=c)
        vo=ProductVoice.objects.filter(is_active=True,category=c)
        f=ProductFile.objects.filter(is_active=True,category=c)

        v_ser=VideoSerializer(instance=v,many=True)
        vo_ser=VoiceSerializer(instance=vo,many=True)
        f_ser=FileProductSerializer(instance=f,many=True)
        z=[]
        z.extend([
            v_ser.data,
            vo_ser.data,
            f_ser.data
        ])
        return Response(z)
    
        

    
    


