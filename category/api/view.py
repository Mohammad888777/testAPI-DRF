from django.shortcuts import get_object_or_404
from rest_framework.serializers import ValidationError
from .serializers import CategoryFirstSerializer,SubCategorySerializer,FreeCatSerializer,EachPaySerializer
from ..models import Category
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count,Avg,Q,F,BooleanField,Value
from datetime import datetime,timedelta
from rest_framework.authtoken.models import Token
from account.models import User
from django.conf import settings
import jwt
from django.db.models.expressions import When,Case
from rest_framework.decorators import api_view,permission_classes,authentication_classes,throttle_classes
from account.api.permissions import CustomLoginPermission
from account.api.authentications import CombineAuthentication
from card.models import CartItem,Cart
from ..paginatons import CustomPagination
from ..utils import hande_paginator




class Home(GenericAPIView,ListModelMixin):
    lookup_field="id"
    

    def get_queryset(self):
        return Category.objects.filter(
            is_active=True,
            parent__isnull=True,
            category_type="0"
        )
    def get_serializer_class(self):
        return CategoryFirstSerializer
    
    def get(self,request,*args,**kwargs):
        q=self.get_queryset()
        s=self.get_serializer_class()(instance=q,many=True,context={'request':request})
        return Response(s.data)
    







class EachCategory(APIView):
     

    def get(self,request,*args,**kwargs):

        order_by=self.request.GET.get("ord","d")
        ord_by="created" if order_by=="d" else "-created"
        is_finshed_cats=self.request.GET.get("fin",False)
        min_price=self.request.GET.get("min",0)
        max_price=self.request.GET.get("min",100000000)
        page=self.request.GET.get("page",1)
        perPage=self.request.GET.get("perPage",1)
        

        q=get_object_or_404(Category,
                            id=self.kwargs.get("id"),
                            category_type="0",
                            parent__isnull=True,
                            is_active=True
                            )
        q_child=None
        is_user_logged_in=self.user_is_logged_in_or_not()

        if not is_user_logged_in:

            q_child=q.children.all().filter(is_active=True,category_type="0").annotate(
                avg=Avg("reviewrating__rating",filter=Q(reviewrating__is_active=True)),
                add_to_cart=Value(False),
                saved_in=Value(False)
            ).order_by(
                ord_by
            ).filter(
                Q(is_active=is_finshed_cats) if is_finshed_cats else Q()
            ).filter(
                Q(price__range=(int(min_price),int(max_price)))
            )

        else:



            user=get_object_or_404(User,id=is_user_logged_in[1])
            user_cart=get_object_or_404(Cart,cart_id_custom=str(user.id))

            use_cart_items=CartItem.objects.filter(
                cart=user_cart,
                user=user,
            )
            ids=[]
            for i in use_cart_items:
                ids.append(str(i.category.id))
            

            q_child=q.children.all().filter(
                is_active=True
                ).annotate(
                avg=Avg("reviewrating__rating",filter=Q(reviewrating__is_active=True)),
                    saved_in=Case(
                        When(Q(saves__id__icontains=str(user.id)),then=True),
                        When(~Q(saves__id__icontains=str(user.id)),then=False),
                        output_field=BooleanField()
                    ),
                    add_to_cart=Case(
                        When(Q(id__in=ids),True),
                        When(~Q(id__in=ids),False),
                        output_field=BooleanField()
                    )
            ).order_by(
                ord_by
            ).filter(
                Q(category_type="0")&
                Q(is_active=is_finshed_cats) if is_finshed_cats else Q()
            ).filter(
                Q(price__range=(int(min_price),int(max_price)))
            )
        h_pagin=hande_paginator(q_child,page=page,perPage=perPage)
        s=SubCategorySerializer(instance=h_pagin,many=True,context={'request':request})

        return Response(s.data)




    def user_is_logged_in_or_not(self):
        _token=self.request.META.get("HTTP_TOKEN")
        _jt=self.request.META.get("HTTP_AUTHORIZATION")
        check_t=None

        if _jt:
            check_t=''.join(list([str(i) for i in _jt][7:]))
            if _token:
                print("AAAAAAAAAAAAAAA")
                try:
                    payload=jwt.decode(jwt=check_t,key=settings.SECRET_KEY,algorithms=['HS256'])
                    print("BBBBBBBBBBB")
        
                    converted_tie=datetime.fromtimestamp(payload.get("exp"))
                    print(converted_tie,"MMMMMMMMMMMM")
                    now=datetime.now()

                    if converted_tie <now:
                        print("CCCCCCCCCCCCC")
                        return False
                    
                    try:
                        founded_user=User.objects.get(id=payload.get("user_id"))
                        print("DDDDDDDDDDDDDDDDD")
                    except Exception as e:
                        return False
                    try:
                        user_t=Token.objects.get(key=_token,user=founded_user)
                        print("EEEEEEEEEEEEEEEEEE")
                        return True,str(user_t.user.id)
                    except Exception as e:
                        return False
                    
                except Exception as e:

                    return False

            else:
                return False
        else:
            return False




@api_view(["POST"])
@permission_classes([CustomLoginPermission])
@authentication_classes([CombineAuthentication])
def save_cat(request,id):
    user=request.user
    cat=get_object_or_404(Category.objects.annotate(
        saved_in=Case(
                        When(Q(saves__id__icontains=str(user.id)),then=True),
                        When(~Q(saves__id__icontains=str(user.id)),then=False),
                        output_field=BooleanField()
                    )
    ),parent__isnull=False,id=id,is_active=True)
    saved=False
    if user in cat.saves.all():
        cat.saves.remove(user)
        cat.save()
        saved=False
    else:
        cat.saves.add(user)
        cat.save()
        saved=True
    return Response({
        "saved":saved
    })

        




class FreeCats(APIView):

    def get(self,request,*args,**kwargs):
        
        
        q_child=None
        is_user_logged_in=self.user_is_logged_in_or_not()

        if not is_user_logged_in:

            q_child=Category.objects.filter(
                            is_active=True,
                            parent__isnull=True,
                            category_type="1",
            ).filter(is_active=True).annotate(
                cc=Avg("price"),
                add_to_cart=Value(False)
            ).order_by(
                "created"
            )

        else:



            user=get_object_or_404(User,id=is_user_logged_in[1])
            user_cart=get_object_or_404(Cart,cart_id_custom=str(user.id))

            use_cart_items=CartItem.objects.filter(
                cart=user_cart,
                user=user,
            )
            ids=[]
            for i in use_cart_items:
                ids.append(str(i.category.id))
            

            q_child=Category.objects.filter(
                            is_active=True,
                            parent__isnull=True,
                            category_type="1",
            ).annotate(
                    cc=Avg("price"),
                    saved_in=Case(
                        When(Q(saves__id__icontains=str(user.id)),then=True),
                        When(~Q(saves__id__icontains=str(user.id)),then=False),
                        output_field=BooleanField()
                    ),
                    add_to_cart=Case(
                        When(Q(id__in=ids),True),
                        When(~Q(id__in=ids),False),
                        output_field=BooleanField()
                    )
            ).order_by(
                "created"
            )

        s=FreeCatSerializer(instance=q_child,many=True,context={'request':request})
        return Response(s.data)
    


    def user_is_logged_in_or_not(self):
        _token=self.request.META.get("HTTP_TOKEN")
        _jt=self.request.META.get("HTTP_AUTHORIZATION")
        check_t=None

        if _jt:
            check_t=''.join(list([str(i) for i in _jt][7:]))
            if _token:
                print("AAAAAAAAAAAAAAA")
                try:
                    payload=jwt.decode(jwt=check_t,key=settings.SECRET_KEY,algorithms=['HS256'])
                    print("BBBBBBBBBBB")
        
                    converted_tie=datetime.fromtimestamp(payload.get("exp"))
                    print(converted_tie,"MMMMMMMMMMMM")
                    now=datetime.now()

                    if converted_tie <now:
                        print("CCCCCCCCCCCCC")
                        return False
                    
                    try:
                        founded_user=User.objects.get(id=payload.get("user_id"))
                        print("DDDDDDDDDDDDDDDDD")
                    except Exception as e:
                        return False
                    try:
                        user_t=Token.objects.get(key=_token,user=founded_user)
                        print("EEEEEEEEEEEEEEEEEE")
                        return True,str(user_t.user.id)
                    except Exception as e:
                        return False
                    
                except Exception as e:

                    return False

            else:
                return False
        else:
            return False







class EachFreePackage(
    RetrieveModelMixin,GenericAPIView
):
    
    def get_queryset(self):
        return Category.objects.filter(
            category_type="1",
            is_active=True,
        )
    
    def get_object(self):
        q=self.get_queryset()
        return get_object_or_404(q,id=self.kwargs.get("id"))
    
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    def get_serializer_class(self):
        return FreeCatSerializer
    





class AllPayPackage(
    ListModelMixin,GenericAPIView
):
    

    def get_queryset(self):
        return Category.objects.filter(
            category_type="0",
            parent__isnull=False,is_active=True,
        )
    
    def get_serializer_class(self):
        return SubCategorySerializer
    

    def get(self,request,*args,**kwargs):
        user_logged_in=self.user_is_logged_in_or_not()
        page=self.request.GET.get("page",1)
        perPage=self.request.GET.get("perPage",1)

        if not user_logged_in:

            q=self.get_queryset().annotate(
                avg=Avg("reviewrating__rating",filter=
                        Q(reviewrating__is_active=True)
                        ),
                add_to_cart=Value(False),
                saved_in=Value(False)
            )
        else:
            user=get_object_or_404(User,id=user_logged_in[1])
            user_cart=get_object_or_404(Cart,cart_id_custom=str(user.id))

            use_cart_items=CartItem.objects.filter(
                cart=user_cart,
                user=user,
            )
            ids=[]
            for i in use_cart_items:
                ids.append(str(i.category.id))

            q=self.get_queryset().annotate(
                avg=Avg("reviewrating__rating",filter=Q(reviewrating__is_active=True)),
                saved_in=Case(
                    When(Q(saves__id__icontains=str(user.id)),then=True),
                    When(~Q(saves__id__icontains=str(user.id)),then=False),
                    output_field=BooleanField()
                ),
                add_to_cart=Case(
                    When(Q(id__in=ids),True),
                    When(~Q(id__in=ids),False),
                    output_field=BooleanField()
                )
            )
        
        paging_q=hande_paginator(q,perPage=perPage,page=page)
        
        s=self.get_serializer_class()(instance=paging_q,many=True,context={'request':request})
        return Response(s.data)
    
    
    def user_is_logged_in_or_not(self):
        _token=self.request.META.get("HTTP_TOKEN")
        _jt=self.request.META.get("HTTP_AUTHORIZATION")
        check_t=None

        if _jt:
            check_t=''.join(list([str(i) for i in _jt][7:]))
            if _token:
                print("AAAAAAAAAAAAAAA")
                try:
                    payload=jwt.decode(jwt=check_t,key=settings.SECRET_KEY,algorithms=['HS256'])
                    print("BBBBBBBBBBB")
        
                    converted_tie=datetime.fromtimestamp(payload.get("exp"))
                    print(converted_tie,"MMMMMMMMMMMM")
                    now=datetime.now()

                    if converted_tie <now:
                        print("CCCCCCCCCCCCC")
                        return False
                    
                    try:
                        founded_user=User.objects.get(id=payload.get("user_id"))
                        print("DDDDDDDDDDDDDDDDD")
                    except Exception as e:
                        return False
                    try:
                        user_t=Token.objects.get(key=_token,user=founded_user)
                        print("EEEEEEEEEEEEEEEEEE")
                        return True,str(user_t.user.id)
                    except Exception as e:
                        return False
                    
                except Exception as e:

                    return False

            else:
                return False
        else:
            return False




class EachPayPackage(
    APIView
):
    
    def get(self,request,*args,**kwargs):
        c=get_object_or_404(
            Category.objects.annotate(
                has_videos=Case(
                    When(
                        Q(productvideo__isnull=False)&Q(productvideo__is_active=True),then=True
                    ),
                    When(
                        Q(productvideo__isnull=True)&Q(productvideo__is_active=True),then=False
                    ),
                    default=False, 
                    output_field=BooleanField()
                ),
                has_voices=Case(
                    When(
                        Q(productvoice__isnull=False)&Q(productvoice__is_active=True),then=True
                    ),
                    When(
                        Q(productvoice__isnull=True)&Q(productvoice__is_active=True),then=False
                    ),
                    default=False, 
                    output_field=BooleanField()
                ),
                has_files=Case(
                    When(
                        Q(productfile__isnull=False)&Q(productfile__is_active=True),then=True
                    ),
                    When(
                        Q(productfile__isnull=True)&Q(productfile__is_active=True),then=False
                    ),
                    default=False, 
                    output_field=BooleanField()
                )
            ),
            parent__isnull=False,
            id=self.kwargs.get("id"),
            category_type="0",
            is_active=True
        )
        ser=EachPaySerializer(instance=c,context={'request': request})
        return Response(ser.data)
    

