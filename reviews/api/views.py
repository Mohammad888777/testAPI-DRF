from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework.response import Response
from ..models import ReviewRating,ReviewBlog
from .serializers import ReviewSerializer,SubReviewSerializer,ReviewBlogSerializer,SubBlogReviewSerializer
from django.shortcuts import get_object_or_404
from category.models import Category
from django.db import transaction
from rest_framework.views import APIView
from account.mixins import UserNotBeBlocked,UserNotBeBlockedForEver
from account.api.authentications import CombineAuthentication
from account.api.permissions import CustomLoginPermission
from account.throttle import RegisterThrottle
from category.utils import hande_paginator
from blogs.models import Blog





class MainFreeCatsReview(ListAPIView):
    def get_queryset(self):
        
        return ReviewRating.objects.filter(
            is_active=True,
            category__category_type="1"
        )
    def get_serializer_class(self):
        return ReviewSerializer
    
    def list(self, request, *args, **kwargs):
        limit=request.query_params.get("limit",0)
        offset=request.query_params.get("offset",2)

        q=self.get_queryset()[int(limit):int(limit)+int(offset)]
        s=self.get_serializer_class()(instance=q,many=True)
        return Response(s.data)
        



class EachFreeCatReview(
    GenericAPIView,ListModelMixin
):
    
    def get_queryset(self):
        cat=get_object_or_404(Category,
                              is_active=True,
                              category_type="1",
                              id=self.kwargs.get("id")
                              )
        return ReviewRating.objects.filter(
            category=cat,
            is_active=True
        )
    def get_serializer_class(self):
        return ReviewSerializer
    
    def get(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)
    
     
    


class MakeFreeReviewMainPage(
    UserNotBeBlocked,
    UserNotBeBlockedForEver,
    APIView   
):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]
    
    def get_throttles(self):
        throttle_classes=[RegisterThrottle]
        return [i() for i in throttle_classes]
    
        

    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            data:dict=request.data
            user=request.user
            new_rev=SubReviewSerializer(data=data)
            new_rev.is_valid(raise_exception=True)
            n=new_rev.save()
            n.user=user
            n.review_type="1"
            n.save()
            return Response(new_rev.data)


class MakeFreeReviewEachPackage(
    UserNotBeBlocked,UserNotBeBlockedForEver,
    APIView
):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]
    
    def get_throttles(self):
        throttle_classes=[RegisterThrottle]
        return [i() for i in throttle_classes]
    def post(self,request,*args,**kwargs):

        with transaction.atomic():
            c=get_object_or_404(
                Category,
                is_active=True,
                id=self.kwargs.get("id"),
                category_type="1",
                parent__isnull=True
                                )
            
            data:dict=request.data
            user=request.user
            new_rev=SubReviewSerializer(data=data)
            new_rev.is_valid(raise_exception=True)
            n=new_rev.save()
            n.user=user
            n.review_type="1"
            n.category=c
            n.save()
            return Response(new_rev.data)



# from here 


class ReplayFreeCommet(APIView):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]
    
    def get_throttles(self):
        throttle_classes=[RegisterThrottle]
        return [i() for i in throttle_classes]
    
        

    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            r=get_object_or_404(ReviewRating,
                                id=self.kwargs.get("id"),
                                is_active=True,
                                )
            data:dict=request.data
            user=request.user
            new_rev=SubReviewSerializer(data=data)
            new_rev.is_valid(raise_exception=True)
            n=new_rev.save()
            n.user=user
            n.review_type="1"
            n.parent=r
            n.save()
            return Response(new_rev.data)


class ReplayEachFreePackageComment(APIView):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]
    
    def get_throttles(self):
        throttle_classes=[RegisterThrottle]
        return [i() for i in throttle_classes]
    def post(self,request,*args,**kwargs):

        with transaction.atomic():
            c=get_object_or_404(
                Category,
                is_active=True,
                id=self.kwargs.get("id"),
                category_type="1",
                parent__isnull=True
                                )
            r=get_object_or_404(ReviewRating,
                                id=self.kwargs.get("c_id"),
                                is_active=True,
                                category=c
                                )
            
            data:dict=request.data
            user=request.user
            new_rev=SubReviewSerializer(data=data)
            new_rev.is_valid(raise_exception=True)
            n=new_rev.save()
            n.user=user
            n.review_type="1"
            n.category=c
            n.parent=r
            n.save()
            return Response(new_rev.data)



class EachBlocgComments(APIView):

    def get(self,request,*args,**kwargs):

        b=get_object_or_404(
            Blog,
            id=self.kwargs.get("id"),
            is_active=True
                            )
        r=ReviewBlog.objects.filter(
            blog=b,
            is_active=True
        )
        s=ReviewBlogSerializer(instance=r,many=True)

        return Response(s.data)
    
        
        



class AddCommentForEachBlog(APIView):

    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]
    
    def get_throttles(self):
        throttle_classes=[RegisterThrottle]
        return [i() for i in throttle_classes]
    def post(self,request,*args,**kwargs):

        with transaction.atomic():
            
            b=get_object_or_404(
                Blog,
                is_active=True,
                id=self.kwargs.get("id"),    
            )
            
            data:dict=request.data
            user=request.user
            new_rev=SubBlogReviewSerializer(data=data)
            new_rev.is_valid(raise_exception=True)
            n=new_rev.save()
            n.user=user
            n.blog=b
            n.save()
            return Response(new_rev.data)




class ReplayCommentOfEachBlog(APIView):
    permission_classes=[CustomLoginPermission]
    authentication_classes=[CombineAuthentication]
    
    def get_throttles(self):
        throttle_classes=[RegisterThrottle]
        return [i() for i in throttle_classes]
    def post(self,request,*args,**kwargs):

        with transaction.atomic():
            b=get_object_or_404(
                Blog,
                is_active=True,
                id=self.kwargs.get("b_id"),
                                )
            
            r=get_object_or_404(ReviewBlog,
                                id=self.kwargs.get("id"),
                                is_active=True,
                                blog=b
                                )
            data:dict=request.data
            user=request.user
            new_rev=SubBlogReviewSerializer(data=data)
            new_rev.is_valid(raise_exception=True)
            n=new_rev.save()
            n.user=user
            n.blog=b
            n.parent=r
            n.save()
            return Response(new_rev.data)



class EachPayComments(APIView):
    
    def get(self,request,*args,**kwargs):
        c=get_object_or_404(
            Category,
            category_type="0",
            is_active=True,
            id=self.kwargs.get("id")
        )
        r=ReviewRating.objects.filter(
            category=c,
            is_active=True
        )
        s=ReviewSerializer(instance=r,many=True)
        return Response(s.data)
    


class AddCommentForEachPayPackage(APIView):
    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            c=get_object_or_404(
                Category,
                id=self.kwargs.get("id"),
                category_type="0",
                is_active=True
            )
            data:dict=request.data
            user=request.user
            new_rev=SubReviewSerializer(data=data)
            new_rev.is_valid(raise_exception=True)
            n=new_rev.save()
            n.user=user
            n.review_type="0"
            n.category=c
            n.save()
        
            return Response(new_rev.data)
        

class ReplayCommentsForEachPayPackage(APIView):

    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            c=get_object_or_404(
                Category,
                id=self.kwargs.get("id"),
                category_type="0",
                is_active=True
            )
            r=get_object_or_404(
                ReviewRating,
                id=self.kwargs.get("r_id"),
                is_active=True,
                category=c
                                )
            data:dict=request.data
            user=request.user
            new_rev=SubReviewSerializer(data=data)
            new_rev.is_valid(raise_exception=True)
            n=new_rev.save()
            n.user=user
            n.review_type="0"
            n.category=c
            n.parent=r
            n.save()
        
            return Response(new_rev.data)


