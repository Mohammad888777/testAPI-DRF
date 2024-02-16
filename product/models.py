from django.db import models
import uuid
from category.models import Category




class ProductVideo(models.Model):
    
    id = models.UUIDField(

         verbose_name="ای دی ویدیو",
         help_text="ای دی ویدیو",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True

    )

    category=models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        verbose_name="دسته بندی",
        help_text="دسته بندی",
        db_index=True,null=True,
        blank=True
    )

    part=models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="قسمت",
        help_text="قسمت",
        db_index=True
    )

    is_active = models.BooleanField( 
                                        db_index = True ,
                                        verbose_name = "فعال است" ,
                                        help_text = "فعال است",
                                        default=False,
                                        null=True,
                                        blank=True

                                    )



    video_duration=models.CharField(
        verbose_name="دقایق فیلم",
        help_text="دقایق فیلم",
        db_index=True,
        max_length=50

    )

    video_link=models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک",
        help_text="لینک",
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


    is_active.bool=True



    def __str__(self) -> str:
        return str(self.category)
    
    class Meta:
        verbose_name ="فیلم ها"
        verbose_name_plural ="فیلم ها"
        ordering=["updated"]



class ProductVoice(models.Model):
    
    id = models.UUIDField(

         verbose_name="ای دی ویس",
         help_text="ای دی ویس",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True

    )

    category=models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        verbose_name="دسته بندی",
        help_text="دسته بندی",
        db_index=True,null=True,
        blank=True
    )

    part=models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="قسمت",
        help_text="قسمت",
        db_index=True
    )

    is_active = models.BooleanField( 
                                        db_index = True ,
                                        verbose_name = "فعال است" ,
                                        help_text = "فعال است",
                                        default=False,
                                        null=True,
                                        blank=True

                                    )

    voice=models.FileField(
        verbose_name="ویس",
        help_text="ویس",
        db_index=True,
        null=True,
        blank=True
    )

    voice_duration=models.CharField(
        verbose_name="دقایق ویس",
        help_text="دقایق ویس",
        db_index=True,
        max_length=50
    
    )

    voice_link=models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک",
        help_text="لینک",
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


    is_active.bool=True



    def __str__(self) -> str:
        return str(self.category)
    
    class Meta:
        verbose_name ="ویس ها"
        verbose_name_plural ="ویس ها"
        ordering=["updated"]



class ProductFile(models.Model):
    
    id = models.UUIDField(

         verbose_name="ای دی فایل",
         help_text="ای دی فایل",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True

    )

    category=models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        verbose_name="دسته بندی",
        help_text="دسته بندی",
        db_index=True,null=True,
        blank=True
    )

    file_name =models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="نام فایل",
        help_text="نام فایل",
    )

    part=models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="قسمت",
        help_text="قسمت",
        db_index=True
    )
    

    is_active = models.BooleanField( 
                                        db_index = True ,
                                        verbose_name = "فعال است" ,
                                        help_text = "فعال است",
                                        default=False,
                                        null=True,
                                        blank=True

                                    )

    product_file=models.FileField(
        verbose_name="فایل",
        help_text="فایل",
        db_index=True,
        null=True,blank=True
    )



    file_link=models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک",
        help_text="لینک",
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

    is_active.bool=True
  
    def __str__(self) -> str:
        return str(self.category)
    
    class Meta:
        verbose_name ="فایل ها"
        verbose_name_plural ="فایل ها"
        ordering=["updated"]



