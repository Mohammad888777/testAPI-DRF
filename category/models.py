from django.db import models
import uuid
from django.utils.text import slugify
from account.models import User
from ckeditor_uploader.fields import RichTextUploadingField


PRODUCT_TYPE=(
    ("حضوری","حضوری"),
    ("غیرحضوری","غیرحضوری"),
    ("online","online"),
)


CATEGORY_TYPE=(
    ("0","pay"),
    ("1","free"),
)



class Copon(models.Model) : 
    
    id = models.UUIDField(

         verbose_name="ای دی کوپون",
         help_text="ای دی کوپون",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True

    )

    copone_code = models.CharField(

        max_length=4,
        verbose_name="کد تخفیف",
        help_text="کد تخفیف",
        db_index=True,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
                                default = False ,
                                help_text = "فعال است ؟",
                                verbose_name = "فعال است",
                                db_index = True,
                            
                          )

    number = models.PositiveIntegerField(
        verbose_name="تعداد",
        help_text="تعداد",
    )

    expire_time=models.DateTimeField()

    off_percent= models.PositiveIntegerField(
        null=True,blank=True,
        help_text="درصد تخفیف",
        verbose_name="درصد تخفیف",
    )

    created = models.DateTimeField( 
                                    auto_now_add = True ,
                                    help_text = "زمان ساخت",
                                    verbose_name = "زمان ساخت",
                                    db_index = True,

                                  ) 
      
    updated = models.DateTimeField( 
                                    auto_now = True ,
                                    help_text = "زمان ارتقا",
                                    verbose_name = "زمان ارتقا",
                                    db_index = True,
                                  )


 

    is_active.bool=True

    def __str__(self) -> str:
        return " کد تخفیف  :  "+str(self.copone_code)


    def save(self,*args,**kwargs):
        # self.copone_code=generate_copon()

        return super().save(*args,**kwargs)

    class Meta:
        verbose_name ="کد های تخفیف"
        verbose_name_plural ="کد های تخفیف"
        ordering=["created"]



class SpecialCopon(models.Model):


    id = models.UUIDField(

         verbose_name="ای دی  کوپون اختصاصی",
         help_text="ای دی  کوپون اختصاصی",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True

    )

    copone_code = models.CharField(

        max_length=4,
        verbose_name="کد تخفیف",
        help_text="کد تخفیف",
        db_index=True,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
                                default = False ,
                                help_text = "فعال است ؟",
                                verbose_name = "فعال است",
                                db_index = True,
                            
                          )
    
    off_percent= models.PositiveIntegerField(
        null=True,blank=True,
        help_text="درصد تخفیف",
        verbose_name="درصد تخفیف",
    )

    expired=models.BooleanField(
        default=False,
        verbose_name="منقضی شده",
        help_text="منقضی شده",
    )

    user=models.ForeignKey(
        to=User
        ,
        verbose_name="کاربر",
        help_text="کاربر",
        db_index=True,
        on_delete=models.CASCADE
    )


    created = models.DateTimeField( 
                                    auto_now_add = True ,
                                    help_text = "زمان ساخت",
                                    verbose_name = "زمان ساخت",
                                    db_index = True,

                                  ) 
    
    
    updated = models.DateTimeField( 
                                    auto_now = True ,
                                    help_text = "زمان ارتقا",
                                    verbose_name = "زمان ارتقا",
                                    db_index = True,
                                  )


    

    is_active.bool=True
    expired.bool=True


    def __str__(self) -> str:
        return str(self.copone_code)+str(self.user)
    






    class Meta:
        verbose_name ="کد های  تخفیف اختصاصی"
        verbose_name_plural ="کد های  تخفیف اختصاصی"
        ordering=["created"]




class Teacher(models.Model):
    
    id = models.UUIDField(
         verbose_name="ای دی معلم",
         help_text="ای دی معلم",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True
         )

    name = models.CharField(    
                                max_length = 50,
                                verbose_name = "نام معلم",
                                help_text = "نام معلم را ئارد کنید",
                                db_index = True,
                                # validators = [validate_char]
                           ) 

    slug=models.SlugField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="اسلاگ",
        help_text="اسلاگ",
    )

    image = models.ImageField(
        null=True,
        blank=True
    )


    created = models.DateTimeField( 
                                    auto_now_add = True ,
                                    help_text = "زمان ساخت",
                                    verbose_name = "زمان ساخت",
                                    db_index = True,

                                  ) 
    
    
    updated = models.DateTimeField( 
                                    auto_now = True ,
                                    help_text = "زمان ارتقا",
                                    verbose_name = "زمان ارتقا",
                                    db_index = True,
                                  )
    

    def __str__(self) -> str:

        return str(self.name)
    


    


    def save(self,*args,**kwargs):
        
        if not self.slug:
            self.slug=slugify(self.name, allow_unicode=True)
        
        return super().save(*args,**kwargs)

    class Meta:
        verbose_name ="معلم ها"
        verbose_name_plural ="معلم ها"
        ordering=["updated"]



class TeacherFeather(models.Model):
    
    id = models.UUIDField(
         verbose_name="ای دی ",
         help_text="ای دی ",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True
         )

    detail = models.TextField(    
                                # max_length = 50,
                                verbose_name = "مشخصات",
                                help_text = "مشخصات",
                                db_index = True,
                                # validators = [validate_char]
                           ) 
    teacher=models.ForeignKey(
        Teacher,on_delete=models.CASCADE,
        db_index=True,
        verbose_name=" معلم",
        help_text=" معلم",
    )

    created = models.DateTimeField( 
                                    auto_now_add = True ,
                                    help_text = "زمان ساخت",
                                    verbose_name = "زمان ساخت",
                                    db_index = True,

                                  ) 
    
    
    updated = models.DateTimeField( 
                                    auto_now = True ,
                                    help_text = "زمان ارتقا",
                                    verbose_name = "زمان ارتقا",
                                    db_index = True,
                                  )

    

    
    def __str__(self) -> str:

        return str(self.teacher)
    

    class Meta:
        verbose_name ="مشخصات مدرس"
        verbose_name_plural ="مشخصات مدرس"
        ordering=["created"]


class Category(models.Model):

    id = models.UUIDField(
         verbose_name="ای دی دسته بندی",
         help_text="ای دی دسته بندی",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True
         )

    parent = models.ForeignKey( 
                                to="self", on_delete=models.PROTECT,
                                db_index = True ,
                                verbose_name = "سر دسنه بندی",
                                help_text = "سر دسنه بندی",
                                blank = True,
                                null = True,
                                related_name="child"
                              )

    teacher=models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name="مدرس دوره",
        help_text="مدرس دوره",
        db_index = True,
        null=True,
        blank=True
    )

    saves=models.ManyToManyField(
        to=User,
        blank=True,
        verbose_name="سیو شده",
        help_text="سیو شده",
        db_index = True,
    )

    ckedit=RichTextUploadingField(
         null=True,
         blank=True,db_index=True
    )
    
    name = models.CharField(    
                                max_length = 250,
                                verbose_name = "نام دسته بندی",
                                help_text = "نام دسته بندی را وارد کنید",
                                db_index = True,
                                # validators = [validate_char]
                           ) 

    slug=models.SlugField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="اسلاگ",
        help_text="اسلاگ",
    )

    package_contacts =models.CharField(
        max_length=250,
        db_index=True,
        null=True,
        blank=True,
        verbose_name="مخاطبین دوره",
        help_text="مخاطبین دوره",

    )

    subject =models.TextField(
        
        db_index=True,
        null=True,
        blank=True,
        verbose_name="موضوع آموزش",
        help_text="موضوع آموزش",

    )

    # featured_of_package=models.TextField(
    #     null=True,blank=True,
    #     db_index=True,
    #     verbose_name="مزایا",
    #     help_text="مزایا",
    # )
    
    is_active = models.BooleanField(
                                default = False ,
                                help_text = "فعال است ؟",
                                verbose_name = "فعال است",
                                db_index = True,
                          )
    
   
    
    category_duration = models.TimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="مدت زمان",
        help_text="مدت زمان"

    )

    session_numbers=models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="تعداد جلسات",
        db_index=True,
        help_text="تعداد جلسات",
    )

    description = models.TextField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="توضیحات",
        help_text="توضیحات"
    )

    price=models.FloatField(
        verbose_name="قیمت",
        help_text="قیمت",
        db_index=True,
        null=True,blank=True,
        
    )

    show_price=models.FloatField(
        verbose_name="قیمت اف خورده",
        help_text="قیمت اف خورده",
        db_index=True,
        null=True,blank=True,
        
    )

    category_type=models.CharField(
        max_length=1,
        default="0",
        db_index=True,
        choices=CATEGORY_TYPE,
        verbose_name="نوع دسته بندی",
        help_text="نوع دسته بندی",

    )

    product_type = models.CharField(
                        max_length=10,  
                        choices=PRODUCT_TYPE,
                        default="غیرحضوری",
                        db_index=True,
                        verbose_name="نوع محصول",
                        help_text="نوع محصول",
    )

    pre_review=models.URLField(
        null=True,
        blank=True,
        db_index=True,
        help_text="پیش نمایش",
        verbose_name="پیش نمایش",


    )    

    image = models.ImageField(
        null=True,
        blank=True
    )

    

    created = models.DateTimeField( 
                                    auto_now_add = True ,
                                    help_text = "زمان ساخت",
                                    verbose_name = "زمان ساخت",
                                    db_index = True,

                                  ) 
    
    updated = models.DateTimeField( 
                                    auto_now = True ,
                                    help_text = "زمان ارتقا",
                                    verbose_name = "زمان ارتقا",
                                    db_index = True,
                                  )

    is_active.bool=True

    @property
    def children(self):
        return Category.objects.filter(
            parent=self
        )