from django.urls import path,include

from . import views


urlpatterns=[
    path("api/",include("order.api.urls")),
    path("gateway/<str:order_id>/",views.go_to_gateway_view,name="gateway"),
    path("call-back/<str:order_id>/",views.callback_gateway_view,name="callback-gateway"),
]