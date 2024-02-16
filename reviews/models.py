from django.db import models
import uuid
from account.models import User
from category.models import Category
from blogs.models import Blog



REVIEW_TYPE=(
    ("0","pay"),
    ("1","free"),
)


class ReviewRating(models.Model):
    

    id = models.UUIDField(
         verbose_name="ای دی نظر",
         help_text="ای دی نظر",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True
         )
    
    category=models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        verbose_name="پکیج",
        help_text="پکیج",
        db_index=True,
        null=True,
        blank=True

        )
    

    user=models.ForeignKey(
                        to=User,
                        on_delete=models.PROTECT,
                        verbose_name="کاربر",
                        help_text="کاربر",
                        db_index=True,
                        blank=True,
                        null=True
            )

    parent=models.ForeignKey(
                        to="self",
                        on_delete=models.CASCADE,
                        verbose_name="دسته نظر",
                        help_text="دسته نظر",
                        db_index=True,
                        blank=True,
                        null=True,
                        related_name="child"
            )
 
 
    is_active=models.BooleanField(
        default=False,
        help_text="فعال است ؟",
        verbose_name="فعال است ؟",
        db_index=True,
    )

    review=models.TextField(
                    max_length=200,
                    db_index=True,
                    help_text="نظر",
                    verbose_name="نظر",
        )

    rating=models.FloatField(
        db_index=True,
        help_text="ستاره",
        verbose_name="ستاره",
        null=True,
        blank=True
    )

    name=models.CharField(
        max_length=50,
        null=True,blank=True,
        db_index=True,
        verbose_name="نام",
        help_text="نام",
    )

    review_type=models.CharField(
        max_length=1,
        db_index=True,
        null=True,
        blank=True,
        choices=REVIEW_TYPE,
        default="0",
        verbose_name="review type",
        help_text="review type"
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
        return str(self.category)+str(self.review)
    
    @property
    def children(self):
        return ReviewRating.objects.filter(
            parent=self,is_active=True
        )

    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    class Meta:

        verbose_name="نظرات"
        verbose_name_plural="نظرات"










class ReviewBlog(models.Model):



    id = models.UUIDField(
         verbose_name="ای دی  نظر بلاگ",
         help_text="ای دی  نظر بلاگ",
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
    
    blog=models.ForeignKey(
        to=Blog,
        on_delete=models.PROTECT,
        verbose_name="بلاگ",
        help_text="بلاگ",
        db_index=True,
        null=True,
        blank=True

        )

    name=models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="نام",
        help_text="نام",
    )

    email=models.EmailField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="ایمیل",
        help_text="ایمیل",
    )
    
    parent=models.ForeignKey(
                        to="self",
                        on_delete=models.CASCADE,
                        verbose_name="دسته نظر",
                        help_text="دسته نظر",
                        db_index=True,
                        blank=True,
                        null=True,
                        related_name="child"
            )
    
    review=models.TextField(
                        max_length=25,
                        db_index=True,
                        null=True,
                        blank=True,
                        verbose_name="نظر",
                        help_text="نظر",
        )
    
    is_active=models.BooleanField(
        default=False,
        help_text="فعال است ؟",
        verbose_name="فعال است ؟",
        db_index=True,
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
        return str(self.blog)+str(self.review)
    
    @property
    def children(self):
        return ReviewBlog.objects.filter(
            parent=self,is_active=True
        )
   
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
    class Meta:

        verbose_name="نظرات بلاگ ها"
        verbose_name_plural="نظرات بلاگ ها"

