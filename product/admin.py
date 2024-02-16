from django.contrib import admin
from .models import ProductFile,ProductVideo,ProductVoice

admin.site.register([
    ProductFile,ProductVideo,ProductVoice
])