from django.contrib import admin

from .models import Order,Payment,OrderProduct,FreeOrderProduct



admin.site.register([
    Order,Payment,OrderProduct,FreeOrderProduct
])