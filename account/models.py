from django.db import models
from django.contrib.auth.models import  AbstractBaseUser,PermissionsMixin
import uuid
from django.utils import timezone
from django.core.validators import EmailValidator,validate_email
from .manager import UserManager,TicketManager
from django.core.exceptions import ValidationError
from datetime import datetime,timedelta


def validate_username(value):
    if len(value)<3:
        raise ValidationError("username lenght must be longer than 3")
    return value

# validators 
# def validate_email(value):
#     try:
#         validate_email(value)
#     except Exception as e:
#         print(e)
#         raise ValidationError("email is not correct")
#     if User.objects.filter(email=value).exists():
#         raise ValidationError("email is already exists")
#     return value


def validate_phone(value:str):
    if not 10<=len(value)<=11:
        raise ValidationError("enter valid phone number-phone number length",code=444)
    if not value.isdigit():
        raise ValidationError("enter valid phone number",code=405)
    return value


    
    



class User(AbstractBaseUser,PermissionsMixin):

    id=models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        verbose_name="user id",
        help_text="id",
        db_index=True,
        editable=False
    )

    username=models.CharField(
        max_length=40,
        verbose_name="user username",
        help_text="user username",
        db_index=True,
        null=True,
        blank=True,
        validators=[validate_username]
    )

    email=models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="enter email",
        help_text="enter email"
    )

    phone=models.CharField(
        max_length=11,
        verbose_name="enter phone",
        help_text="enter phone",
        unique=True,
        db_index=True,
        validators=[validate_phone],
    )

    first_name=models.CharField(
        max_length=40,
        db_index=True,
        verbose_name="enter first name",
        help_text="enter first name",
        null=True,
        blank=True,
    )

    last_name=models.CharField(
        max_length=40,
        db_index=True,
        verbose_name="enter last name",
        help_text="enter last name",
        null=True,
        blank=True,
    )

    user_ip=models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="user ip",
        help_text="user ip",
        db_index=True
    )

    date_joined=models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="time joined",
        help_text="time joined",
    )

    is_active=models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="user is active",
        help_text="user is active",
    )

    is_login_now=models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="is user login now",
        help_text="is user login now",
    )

    is_admin=models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="user is admin",
        help_text="user is admin",
    )

    is_staff = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="user is staff",
        help_text="user is staff",
    )

    is_superuser=models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="user is superuser",
        help_text="user is superuser",
    )

    created=models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="time joined",
        help_text="time joined",
    )

    updated=models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name="time updated",
        help_text="time updated",
    )       

    USERNAME_FIELD="phone"
    REQUIRED_FIELDS=["username","email"]
    objects=UserManager()


    def __str__(self) -> str:
        return str(self.phone)
    
    def has_perm(self, perm: str, obj=None ) -> bool:
        return bool(
            self.is_active and self.is_admin or self.is_superuser
        )
    
    def has_module_perms(self, app_label: str) -> bool:
        return bool(
            self.is_active and self.is_admin or self.is_superuser
        )
    
    class Meta:
        ordering=["id"]
        verbose_name="user"
        verbose_name_plural="user"
    




class BlockUser(models.Model):

    id=models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        verbose_name="user id",
        help_text="id",
        db_index=True,
        editable=False
    )

    user=models.OneToOneField(
        null=True,
        blank=True,
        to=User,
        on_delete=models.CASCADE,
        verbose_name="user",
        help_text="user",
        db_index=True
    )

    user_ip=models.GenericIPAddressField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="user ip",
        help_text="user ip",
    )

    blocked_forever=models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="is blocked for ever",
        help_text="is blocked for ever",
    )

    blocked_time=models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    created=models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="time joined",
        help_text="time joined",
    )

    updated=models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name="time updated",
        help_text="time updated",
    ) 


    def __str__(self) -> str:
        return str(self.user_ip)
    

from django.conf import settings

    
class OtpCode(models.Model):

    id=models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        verbose_name="user id",
        help_text="id",
        db_index=True,
        editable=False
    )

    user=models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        db_index=True,
        help_text="user",
        verbose_name="user",
    )

    otp=models.CharField(
        max_length=settings.OTPCODE_LENGTH,
        db_index=True,
        help_text="otp",
        verbose_name="otp",
    )

    expire=models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="expire time",
        verbose_name="expire time",
    )



    created=models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="time joined",
        help_text="time joined",
    )

    updated=models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name="time updated",
        help_text="time updated",
    )

    def save(self,*args,**kwargs):
        self.expire=timezone.now()+timedelta(minutes=2)
        return super().save(*args,**kwargs)
    
    def __str__(self) -> str:
        return str(self.otp)





class MyProfile(models.Model):
    
    id = models.UUIDField(
        verbose_name="ای دی پروفایل",
        help_text="ای دی پروفایل",
        unique=True,
        editable=False,
        default=uuid.uuid4,
        primary_key=True,
        db_index=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="کاربر",
        db_index=True,
        verbose_name="کاربر",
    )

    first_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="اسم",
        db_index=True,
        help_text="اسم را وارد کنید",
        # validators=[validate_char],
    )


    image=models.ImageField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="عکس",
        help_text="عکس",
    )
    
    last_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="فامیلی",
        db_index=True,
        help_text="فامیلی را وارد کنید",
        # validators=[validate_char],
    )

    email = models.EmailField(
        max_length=100,
        verbose_name="ایمیل",
        help_text="ایمیل خود را وارد کنید",
        validators=[],
        db_index=True,
        null=True,
        blank=True,
    )



    created = models.DateTimeField(
        auto_now_add=True,
        help_text="زمان ساخت",
        verbose_name="زمان ساخت",
        db_index=True,
        # TODO
        # must be deleted
        blank=True,
        null=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
        help_text="زمان ارتقا",
        verbose_name="زمان ارتقا",
        db_index=True,
        # TODO
        # must be deleted
        blank=True,
        null=True,
    )



    def __str__(self) -> str:
        return str(self.user)

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل"
        ordering = ["created"]



TICKET_TYPE=(

    ("باز","باز"),
    ("بسته","بسته"),
    ("درحال برسی","درحال برسی"),
    ("پاسخ داده شده","پاسخ داده شده"),

)

EMEGENY_TYPE=(
    ("کم","کم"),
    ("متوسط","متوسط"),
    ("زیاد","زیاد"),
)



class Ticket(models.Model):
    
    id = models.UUIDField(
        verbose_name="ای دی تیکت",
        help_text="ای دی تیکت",
        unique=True,
        editable=False,
        default=uuid.uuid4,
        primary_key=True,
        db_index=True,
    )

    sender_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="ارسال کننده",
        db_index=True,
        verbose_name="ارسال کننده",
        related_name="sender"
    )


    ticket_type=models.CharField(
        max_length=50,
        db_index=True,
        verbose_name="نوع تیکت",
        help_text="نوع تیکت",
        choices=TICKET_TYPE,
        default="باز"
    )

    department_type=models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='دپارتمان‌را‌انتخاب‌کنید',
        help_text='دپارتمان‌را‌انتخاب‌کنید',
    )
    
    department_ticket_type=models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='نوع دیپارتمنت تیکت',
        help_text='نوع دیپارتمنت تیکت',
    )

    subject=models.CharField(
        max_length=250,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="موضوع تیکت",
        help_text="موضوع تیکت",
    )

    emergency_type=models.CharField(
        max_length=30,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="نوع ضروری پیام",
        choices=EMEGENY_TYPE,
        default="کم"
        
    )


    created = models.DateTimeField(
        auto_now_add=True,
        help_text="زمان ساخت",
        verbose_name="زمان ساخت",
        db_index=True,
        # TODO
        # must be deleted
        blank=True,
        null=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
        help_text="زمان ارتقا",
        verbose_name="زمان ارتقا",
        db_index=True,
        # TODO
        # must be deleted
        blank=True,
        null=True,
    )

    objects=TicketManager()

    def __str__(self) -> str:
        return str(self.sender_user)+"  موضوع پیام  : "+str(self.subject)

    class Meta:
        verbose_name = "تیکت ها"
        verbose_name_plural = "تیکت ها"
        ordering = ["created"]



class Message(models.Model):
    
    id = models.UUIDField(
        verbose_name="ای دی تیکت",
        help_text="ای دی تیکت",
        unique=True,
        editable=False,
        default=uuid.uuid4,
        primary_key=True,
        db_index=True,
    )

    sender_messager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="ارسال کننده",
        db_index=True,
        verbose_name="ارسال کننده",
        related_name="sender_messager",
        null=True,
        blank=True
    )

    receiver_messager = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="دریافت کننده",
    )

    ticket=models.ForeignKey(
        on_delete=models.CASCADE,
        to=Ticket,
        db_index=True,
        help_text="تیکت",
        verbose_name="تیکت",
        null=True,
        blank=True,
        
    )

    message_file=models.FileField(
        verbose_name="فایل",
        help_text="فایل",
        db_index=True,
        null=True,
        blank=True,
    )

    message=models.TextField(
        db_index=True,
        help_text="پیغام",
        verbose_name="پیغام",
    )


    created = models.DateTimeField(
        auto_now_add=True,
        help_text="زمان ساخت",
        verbose_name="زمان ساخت",
        db_index=True,
        # TODO
        # must be deleted
        blank=True,
        null=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
        help_text="زمان ارتقا",
        verbose_name="زمان ارتقا",
        db_index=True,
        # TODO
        # must be deleted
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return str(self.ticket)

    

    class Meta:
        verbose_name = "پیغام ها"
        verbose_name_plural = "پیغام ها"
        ordering = ["created"]
