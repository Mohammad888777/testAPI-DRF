from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.response import Response
from ..models import User,OtpCode
from django.shortcuts import get_object_or_404
from django.db import transaction
from ..utils import generate_otp,send_otp
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .authentications import CombineAuthentication
from .permissions import CustomLoginPermission
from ..mixins import (
    UserNotBeBlocked,UserNotBeBlockedForEver,
    NotBeingLoggedIn
)
from django.utils import timezone

from ..tasks import async_send_otp
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime,timedelta

from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login

class UserRegisterOrLogin(
    UserNotBeBlockedForEver,
    UserNotBeBlocked,
    NotBeingLoggedIn,
    CreateModelMixin,
    GenericAPIView
):
    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            data:dict=request.data
            self.before_numb(data=data)
            user=None
            try:
                user=User.objects.select_related("blockuser", "otpcode", "auth_token").get(phone=data.get("phone"))
            except User.DoesNotExist:
                user=None
            
            if user:
                otp=generate_otp()
                try:
                    s1=async_send_otp.signature(countdown=0.5)
                    s1.apply_async(args=[user.phone,otp])
                    return Response({
                        "otp":"sent",
                        "new":False,
                        "user_token":str(user.auth_token.key)
                    })

                except Exception as e:
                    raise ValidationError(f"sendding msg error {e}",code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)
            else:
                new_user=User.objects.create_user(
                    phone=data.get("phone")
                )
                new_user.is_active=True
                new_user.save()
                otp=generate_otp()
                try:
                    s1=async_send_otp.signature(countdown=0.5)
                    s1.apply_async(args=[new_user.phone,otp])
                    return Response({
                        "otp":"sent",
                        "user_token":str(new_user.auth_token.key)
                        
                    })

                except Exception as e:
                    raise ValidationError(f"sendding msg error {e}",code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)

                

    
    def before_numb(self,data:dict):

        if not "phone" in data:
            raise ValidationError("phone is required",code=status.HTTP_204_NO_CONTENT)
        if len(data)>1:
            raise ValidationError("only phone is required",code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
        if not 10<=len(data.get("phone"))<=11:
            raise ValidationError("phone is not correct",code=status.HTTP_304_NOT_MODIFIED)
        if not data.get("phone").isdigit():
            raise ValidationError("phone is not correct",code=status.HTTP_204_NO_CONTENT)




class Login(
    UserNotBeBlockedForEver,
    UserNotBeBlocked,
    APIView
):
    
    authentication_classes=[TokenAuthentication]
    permission_classes=[CustomLoginPermission]

    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            
            data:dict=request.data
            print("####")
            print("####")
            print(data)
            print("####")
            self.before_numb(data=data)
            code=None
            try:
                code=OtpCode.objects.select_related("user","user__blockuser").get(otp=data.get("otp"))
            except OtpCode.DoesNotExist:
                code=None
            
            
            if code:

                now=timezone.now()
                
                if code.expire<now:
                    raise ValidationError("code is expired",code=status.HTTP_404_NOT_FOUND)
            
                ref=RefreshToken.for_user(code.user)
                login(request,code.user)
                code.user.is_login_now=True
                return Response({
                    "access":str(ref.access_token),
                    "refresh":str(ref),
                    "user_token":str(code.user.auth_token.key)
                })

            else:
                raise ValidationError("otp is incorrect",code=status.HTTP_204_NO_CONTENT)


            
            


        return super().dispatch(request, *args, **kwargs)

    def before_numb(self,data:dict):
        if not "otp" in data:
            raise ValidationError("otp is required",code=status.HTTP_204_NO_CONTENT)
        if len(data)>1:
            raise ValidationError("only otp is required",code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
        # if not len(data.get("otp"))!=settings.OTPCODE_LENGTH:
        #     raise ValidationError("otp is not correct",code=status.HTTP_304_NOT_MODIFIED)
        if not data.get("otp").isdigit():
            raise ValidationError("otp is not correct",code=status.HTTP_204_NO_CONTENT)


