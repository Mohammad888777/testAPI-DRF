from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from ..models import User
from rest_framework.authtoken.models import Token
import jwt
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime



class CombineAuthentication(JWTAuthentication):

    def authenticate(self, request):

        _token=request.META.get("HTTP_TOKEN")
        _jt=request.META.get("HTTP_AUTHORIZATION")

        print("@@@@@@@@")
        print("@@@@@@@@")
        print(_jt)
        print(_token)
        print("@@@@@@@@")
        print("@@@@@@@@")
        check_t=None

        if _jt:
            check_t=''.join(list([str(i) for i in _jt][7:]))
            if _token:

                try:
                    payload=jwt.decode(jwt=check_t,key=settings.SECRET_KEY,algorithms=['HS256'])
                    # print(payload.get("user_id"))
                    # print(payload.get("sub"))
                    # print(payload.get("exp"))
                    now=datetime.now()
                    # if  datetime.fromtimestamp(float(payload.get("exp")))<=now:
                    print('##########')
                    print('##########')
                    print(payload.get("user_id"))
                    print('##########')
                    print('##########')
                    if payload.get("exp")<0:
                        print("YEYYEYEYEY")
                        raise ValidationError('token is expired')
                    
                    try:

                        founded_user=User.objects.get(id=payload.get("user_id"))
                    except Exception as e:
                        raise ValidationError("user not found")
                    try:
                        user_t=Token.objects.get(key=_token,user=founded_user)
                    except Exception as e:
                        raise ValidationError("user token not found")
                    
                except Exception as e:

                    raise ValidationError("jwt is required")

            else:
                raise ValidationError("user token is required")

        else:
            raise ValidationError("jwt token is required")



        return super().authenticate(request)


