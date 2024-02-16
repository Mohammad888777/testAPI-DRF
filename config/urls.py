from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/",include("account.urls")),
    path("category/",include("category.urls")),
    path("blogs/",include("blogs.urls")),
    path("card/",include("card.urls")),
    path("order/",include("order.urls")),
    path("reviews/",include("reviews.urls")),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path("bankgateways/", az_bank_gateways_urls()),

]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
