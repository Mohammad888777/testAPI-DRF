from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from .models import User,MyProfile
from django.db import transaction
from card.models import Cart



def auto_create_token(sender,instance,created,**kwargs):

    with transaction.atomic():

        if created:
            Token.objects.create(
                user=instance
            )   
            Cart.objects.create(
                cart_id_custom=str(instance.id)
            )
            MyProfile.objects.create(
                user=instance
            )
            


post_save.connect(auto_create_token,sender=User)
    