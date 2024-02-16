from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Manager



def validate_phone(value:str):
    if 10<=len(value)<=11:
        raise ValidationError("enter valid phone number-phone number length",code=444)
    if not value.isdigit():
        raise ValidationError("enter valid phone number",code=405)
    return value


class UserManager(BaseUserManager):

    def create_user(self,phone,):

        if not phone:
            raise ValidationError("phone is required")
      
      
        user=self.model(
            phone=phone
        )
        user.save(using=self._db)
        user.set_password(user.id)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,email,password,username,phone):
        try:
            validate_email(email)
        except Exception as e:
            raise ValidationError("email validation error")
        
        # try:
        #     validate_phone(phone)
        # except Exception as e:
        #     raise ValidationError("phone is not valid",e)
        
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
        )
        user.save(using=self._db)

        user.set_password(password)

        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.is_staff=True
        
        user.save(using=self._db)

        return user
    
            
    
    





class TicketManager(Manager):


    def opened_tickets(self,user):
        return self.filter(
            ticket_type="باز",sender_user=user
        ).count()

    def closed_tickets(self,user):
        return self.filter(
            ticket_type="بسته",sender_user=user
        ).count()
    

    def inspected_tickets(self,user):
        return self.filter(
            ticket_type="درحال برسی",sender_user=user
        ).count()
    
    def answered_tickets(self,user):
        return self.filter(
            ticket_type="پاسخ داده شده",sender_user=user
        ).count()