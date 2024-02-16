from django.urls import path,include
from . import views

urlpatterns=[
    path("add/<str:id>/",views.AddCart.as_view(),name="add"),
    path("plus/<str:id>/<str:c_id>",views.IncreateCartItem.as_view(),name="plus"),
    path("neg/<str:id>/<str:c_id>/",views.DecreaseCartItem.as_view(),name="neg"),
]