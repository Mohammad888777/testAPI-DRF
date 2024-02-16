from django.db import models
from django.contrib.auth import get_user_model

from card.models import CartItem
from category.models import Category


import uuid,random


User=get_user_model()


ORDER_STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )



HOW_YOU_FOUND_US=(
    ("instagram","instagram"),
    ("what'sapp","what'sapp"),
    ("google","google"),
    ("دوستان","دوستان"),
    ("سایر","سایر"),
)


def generate_order_id(n=7):
    return ''.join(
        random.choices(
            [str(i) for i in range(0,10)],k=n
        )
    )




class Payment(models.Model):
    


    id = models.UUIDField(
         verbose_name="ای دی پرداخت",
         help_text="ای دی پرداخت",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True


    )

    user=models.ForeignKey(

            to=User,
            on_delete=models.PROTECT,
            verbose_name="کاربر",
            help_text="کاربر",
            db_index=True,
            

        )

    bank_status=models.CharField(
                                    max_length=150,
                                    verbose_name="(بانک) وضعیت پرداخت",
                                    help_text="(بانک) وضعیت پرداخت",
                                    db_index=True

                                )
    
    tracking_code=models.CharField(
                                    max_length=150,
                                    verbose_name="(بانک) tracking code",
                                    help_text="(بانک) tracking code",
                                    db_index=True
                                )
    
    bank_name=models.CharField(
                                    max_length=150,
                                    verbose_name="(بانک) درگاه پرداخت",
                                    help_text="(بانک) درگاه پرداخت",
                                    db_index=True
                                )
    
    amount = models.FloatField(
                                db_index=True,
                                verbose_name="مقدار پرداخت شده",
                                help_text="مقدار پرداخت شده",

    )

    created=models.DateTimeField(
                                    auto_now_add = True ,
                                    help_text = "زمان ساخت",
                                    verbose_name = "زمان ساخت",
                                    db_index = True,
                                    null=True,
                                        blank=True
                                )
    
    updated = models.DateTimeField( 
                                    auto_now = True ,
                                    help_text = "زمان ارتقا",
                                    verbose_name = "زمان ارتقا",
                                    db_index = True,
                                    null=True,
                                        blank=True

                                  )

    status=models.CharField(
        max_length=100,
        verbose_name="وضعیت",
        help_text="وضعیت",
        null=True,blank=True
    )


    def __str__(self) -> str:
        return str(self.amount)+str(self.user)
    

    
    class Meta:

        verbose_name = "پرداخت ها"
        verbose_name_plural = "پرداخت ها"
        ordering=["created"]





class Order(models.Model):
    

    id = models.UUIDField(
         verbose_name="ای دی سفارش",
         help_text="ای دی سفارش",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True


    )

    pay_linl=models.URLField(
        max_length=500,
        null=True,
        blank=True,
        db_index=True,
        
    )

    user=models.ForeignKey(

            to=User,
            on_delete=models.PROTECT,
            verbose_name="کاربر",
            help_text="کاربر",
            db_index=True,
            null=True,
            blank=True
        
        )

    payment = models.ForeignKey(
          to=Payment,
          on_delete=models.PROTECT,
          verbose_name="پرداخت",
          help_text="پرداخت",
          db_index=True,
          null=True,
          blank=True
    )

    carts=models.ManyToManyField(
        to=CartItem,
        verbose_name="ایتم ها",
        help_text="ایتم ها",
        db_index=True
    )

    order_custom_id = models.CharField(

                                max_length=20,
                                null=True,
                                blank=True,
                                verbose_name="ای دی",
                                help_text="ای دی",
                                db_index=True
                    )

    name = models.CharField(
                        max_length=15,
                        verbose_name="نام کاربر",
                        help_text=" نام کاربر",
                        db_index=True,
                        null=True,
                        blank=True
        )
    
    last_name = models.CharField(
                        max_length=15,
                        verbose_name="نام خانوادگی کاربر",
                        help_text="نام خانوادگی کاربر",
                        db_index=True,
                        null=True,
                        blank=True
        )
    
    email = models.EmailField(
                                max_length=100,
                                verbose_name="ایمیل",
                                help_text="ایمیل",
                                db_index=True
                              )
    
    order_total = models.FloatField(
                                        db_index=True,
                                        verbose_name="مبلغ پرداخت سفارش",
                                        help_text="مبلغ پرداخت سفارش",
                                        null=True,
                                        blank=True
                                    )

    tax = models.FloatField(
                            null=True,
                            blank=True,
                            db_index=True,
                            help_text="مبلغ مالیات",
                            verbose_name="مبلغ مالیات",
        )

    total_after_use_copon=models.FloatField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="مبلغ پرداخت بعد از کوپون",
        help_text="مبلغ پرداخت بعد از کوپون",

    )

    used_copon=models.BooleanField(
        null=True,
        blank=True,
        db_index=True,
        default=False,
        verbose_name="از کد تخفیف استفاده کرده",
        help_text="از کد تخفیف استفاده کرده",
    )

    status = models.CharField(
                                max_length=10,
                                choices=ORDER_STATUS,
                                default='New',
                                verbose_name="وضعیت سفارش",
                                help_text="وضعیت سفارش",
                                 db_index=True
                            )

    is_ordered = models.BooleanField(
                                        default=False,
                                        verbose_name="سفارش انجام شده ؟",
                                        help_text="سفارش انجام شده ؟",
                                        db_index=True
        )

    created=models.DateTimeField(
                                    auto_now_add = True ,
                                    help_text = "زمان ساخت",
                                    verbose_name = "زمان ساخت",
                                    db_index = True,
                                    null=True,
                                        blank=True
                                )
    
    updated = models.DateTimeField( 
                                    auto_now = True ,
                                    help_text = "زمان ارتقا",
                                    verbose_name = "زمان ارتقا",
                                    db_index = True,
                                    null=True,
                                        blank=True

                                  )

    used_copon.bool=True
    is_ordered.bool=True


    def __str__(self) -> str:
        return str(self.user)+str(self.name)+str(self.payment)
    
    class Meta:
        
        verbose_name = "سفارش ها"
        verbose_name_plural = "سفارش ها"
        ordering=["created"]    







class OrderProduct(models.Model):
    
    id = models.UUIDField(
         verbose_name="ای دی سفارش",
         help_text="ای دی سفارش",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True


    )

    order = models.ForeignKey(
                        to=Order,
                        on_delete=models.PROTECT,
                        verbose_name="سفارش",
                        help_text="سفارش",
                        db_index=True,null=True,
                        blank=True
        )
    
    payment = models.ForeignKey(
                        to=Payment,
                        on_delete=models.PROTECT,
                        verbose_name="پرداخت",
                        help_text="پرداخت",
                        db_index=True,
                        null=True,
                        blank=True
        )
    
    user = models.ForeignKey(
                        to=User,
                        on_delete=models.PROTECT,
                        verbose_name="کاربر",
                        help_text="کاربر",
                        db_index=True
    )

    category = models.ForeignKey(
                        to=Category,
                        on_delete=models.PROTECT,
                        verbose_name="پکیج",
                        help_text="پکیج",
                        db_index=True
    )
    
    quantity = models.PositiveIntegerField(
                        db_index=True,
                        verbose_name="تعداد",
                        help_text="تعداد",
    )

    package_price = models.FloatField(
                db_index=True,
                verbose_name="قیمت پکیج",
                help_text="قیمت پکیج",
    )

    ordered = models.BooleanField(
                                    default=False,
                                    db_index=True,
                                    verbose_name="سفارش انجام شده",
                                    help_text="سفارش انجام شده",
                )

    created=models.DateTimeField(
                                    auto_now_add = True ,
                                    help_text = "زمان ساخت",
                                    verbose_name = "زمان ساخت",
                                    db_index = True,
                                    null=True,
                                        blank=True
                                )
    
    updated = models.DateTimeField( 
                                    auto_now = True ,
                                    help_text = "زمان ارتقا",
                                    verbose_name = "زمان ارتقا",
                                    db_index = True,
                                    null=True,
                                        blank=True

                                  )
    ordered.bool=True
    


    def __str__(self):
        return str(self.category)+str(self.user)
    

    
    class Meta:
        
        verbose_name = "سفارشات پکیج"
        verbose_name_plural = "سفارشات پکیج"
        ordering=["created"]



class FreeOrderProduct(models.Model):
    
    id = models.UUIDField(
         verbose_name="ای دی سفارش رایگان",
         help_text="ای دی سفارش رایگان",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True
    )

    free_category=models.ForeignKey(
        Category,on_delete=models.PROTECT,
        db_index=True,
        verbose_name="دسته بندی رایگان",
        help_text="دسته بندی رایگان",

    )

    user=models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="کاربر",
        help_text="کاربر",
        db_index=True
    )
    
    
    created=models.DateTimeField(
                                    auto_now_add = True ,
                                    help_text = "زمان ساخت",
                                    verbose_name = "زمان ساخت",
                                    db_index = True,
                                    null=True,
                                        blank=True
                                )
    
    updated = models.DateTimeField( 
                                    auto_now = True ,
                                    help_text = "زمان ارتقا",
                                    verbose_name = "زمان ارتقا",
                                    db_index = True,
                                    null=True,
                                        blank=True

                                  )



    def __str__(self):
        return str(self.free_category)+str(self.user)
    
    
    
    class Meta:
        
        verbose_name = "سفارشات پکیج رایگان"
        verbose_name_plural = "سفارشات پکیج رایگان"
        ordering=["created"]