from django.conf import settings
from rest_framework.serializers import ValidationError
import random
from kavenegar import *


def generate_otp(k=settings.OTPCODE_LENGTH):
    return ''.join(
        random.choices([
            str(i) for i in range(0,10)
        ],k=k)
    )



def send_otp(user_phone_number, otp_code):
    try:
        api = KavenegarAPI(
            settings.KAVEHNEGAR_KEY,
        )
        params = {
            "receptor": user_phone_number,
            "template": settings.KAVEHNEGAR_CUSTOM_TEMPLATE_MYSELF_VAR,
            "token": otp_code,
            "type": "sms",
        }
        response = api.verify_lookup(params)

        print("*********************")
        print("*********************")
        print(response)
        print("*********************")
        print("*********************")

    except Exception as e:
        print("ERROROROR")
        print("ERROROROR")
        print(e)
        print("ERROROROR")
        print("ERROROROR")

        raise ValidationError("code not sent")

