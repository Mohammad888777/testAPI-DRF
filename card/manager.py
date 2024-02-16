from django.db.models.manager import Manager
from django.db.models import Sum,F



class CartItemManager(Manager):

    def make_card(self,user):
        return self.filter(
            user=user,is_paid=False
        ).aggregate(
            s=Sum("category__price")*F("quantity")
        ).get("s",0)
