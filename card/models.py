from django.db import models
from category.models import Category
from account.models import User
import uuid
from .manager import CartItemManager



class Cart(models.Model):

    id = models.UUIDField(
         verbose_name="ای دی دسته بندی",
         help_text="ای دی دسته بندی",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True
         )
    
    cart_id_custom=models.CharField(
        max_length=80,
        unique=True,
        db_index=True,
    )


    def __str__(self) -> str:
        return str(self.cart_id_custom)





class CartItem(models.Model):

    id = models.UUIDField(
         verbose_name="ای دی دسته بندی",
         help_text="ای دی دسته بندی",
         unique=True,
         editable=False,
         default=uuid.uuid4,
         primary_key=True,
         db_index=True
         )
    category=models.ForeignKey(
        Category,
        db_index=True,
        on_delete=models.CASCADE,
    )

    cart=models.ForeignKey(
        Cart,on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True
    )

    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True
    )

    quantity=models.PositiveIntegerField(
        null=True,blank=True,
        db_index=True
    )

    is_paid=models.BooleanField(
        default=False,
        db_index=True
    )

    objects=CartItemManager()


    def __str__(self) -> str:
        return str(self.user)