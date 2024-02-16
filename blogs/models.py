from django.db import models


from django.utils.text import slugify
from ckeditor.fields import RichTextField
# from .manager import BlogManager
from ckeditor_uploader.fields import RichTextUploadingField
# from django_softdelete.models import SoftDeleteModel
import uuid


class Blog(models.Model):
    
    id = models.UUIDField(
         verbose_name="ای دی تصویر",
         help_text="ای دی تصویر",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True
    )
     
    description=RichTextUploadingField(
         
    )

    description_show=models.TextField(
        db_index=True,
        null=True,
        blank=True,
        verbose_name="توضیحات برای نمایش",
        help_text="توضیحات برای نمایش",

    )
    title = models.CharField(
         max_length=100,
         null=True,
         blank=True,
         db_index=True,
         verbose_name="موضوع",
         help_text="موضوع",
    )

    slug=models.SlugField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="اسلاگ",
        help_text="اسلاگ",
        unique=True
    )

    is_active = models.BooleanField( 
                                        db_index = True ,
                                        verbose_name ="فعال است ؟",
                                        help_text = "فعال است ؟",
                                        default=False,
                                        null=True,
                                        blank=True

                                   )

    image =models.ImageField(
                              db_index=True,
                              null=True,
                              blank=True,
    )

#     comments = GenericRelation(Comment)
    mobile_image=models.ImageField(
          null=True,
          blank=True,
          verbose_name="عکس سایز موبایل",
          help_text="عکس سایز موبایل",
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

    left_up_home=models.BooleanField(
        default=False,
        db_index=True,
        help_text="  نمایش درسمت چپ بالا" 
    )

    left_down_home=models.BooleanField(
        default=False,
        db_index=True,
        help_text="نمایش درسمت چپ پایین"
    )


#     right_home=models.BooleanField(
#         default=False,
#         db_index=True,
#         help_text="نمایش درسمت راست"
#     )

    one=models.BooleanField(default=False,db_index=True)
    two=models.BooleanField(default=False,db_index=True)
    three=models.BooleanField(default=False,db_index=True)
    four=models.BooleanField(default=False,db_index=True)
    five=models.BooleanField(default=False,db_index=True)


    writer=models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="نویسنده",
        help_text="نویسنده"
    ) 
    
    is_active.bool=True
    one.bool=True
    two.bool=True
    three.bool=True
    four.bool=True
    five.bool=True
    left_up_home.bool=True
    left_down_home.bool=True

    
    
    def __str__(self) -> str:
         return str(self.title)
     
    
    def save(self,*args,**kwargs):
         
         if not self.slug:
            if self.created:
                self.slug=slugify(self.title+str(self.created), allow_unicode=True)
            else:
                self.slug=slugify(self.title+str(self.description_show[:5]), allow_unicode=True)


         return super().save(*args,**kwargs)
    
    class Meta:
        verbose_name="مقالات"
        verbose_name_plural="مقالات"
        