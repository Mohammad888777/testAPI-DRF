from django.contrib import admin

# Register your models here.
from .models import User,OtpCode,BlockUser,MyProfile,Message,Ticket


admin.site.register([
    User,OtpCode,BlockUser,MyProfile,Message,Ticket
])