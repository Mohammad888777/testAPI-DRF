from rest_framework.validators import ValidationError
from rest_framework import status
from django.http import Http404
from .models import User,OtpCode,BlockUser
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils import timezone


class NotBeingLoggedIn():
    def dispatch(self,request,*args,**kwargs):
        
        _token=request.META.get("HTTP_TOKEN")
        _jt=request.META.get("HTTP_AUTHORIZATION")
        if _token or _jt:
            raise ValidationError("user already is logged in",code=status.HTTP_204_NO_CONTENT)
        return super().dispatch(request,*args,**kwargs)
    



class UserNotBeBlocked():

    def dispatch(self,request,*args,**kwargs):
        now=timezone.now()
        user_ip=request.META.get("REMOTE_ADDR")
        b=BlockUser.objects.filter(user_ip=user_ip,blocked_time__gt=now)
        if b.exists():
            raise ValidationError("user alreay blocked",code=status.HTTP_302_FOUND)
        return super().dispatch(request,*args,**kwargs)


class UserNotBeBlockedForEver():
    def dispatch(self,request,*args,**kwargs):
        user_ip=request.META.get("REMOTE_ADDR")
        b=BlockUser.objects.filter(user_ip=user_ip,blocked_forever=True)
        if b.exists():
            raise ValidationError("user alreay blocked for ever",code=status.HTTP_302_FOUND)
        return super().dispatch(request,*args,**kwargs)
