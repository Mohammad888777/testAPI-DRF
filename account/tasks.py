from celery import shared_task
from .utils import send_otp
from .models import User,OtpCode
from django.shortcuts import get_object_or_404


@shared_task(
    name="send otp code",
    bind=True,
)
def async_send_otp(self,user_num,otp):
    try:
        u=get_object_or_404(User,phone=user_num)
        c=OtpCode.objects.filter(user=u)
        c.delete()

        send_otp(user_phone_number=user_num,otp_code=otp)
        c=OtpCode.objects.create(
            user=u,
            otp=otp
        )
    except Exception as e:
        print("EEEEEEEEEEEEE",e)
        self.retry(
            max_retires=5,
            countdown=4
        )