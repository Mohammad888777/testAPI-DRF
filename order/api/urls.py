from django.urls import path,include

from . import views


urlpatterns=[
    path("makeOrder/",views.MakeOrder.as_view(),name="makeOrder"),
    path("createTicket/",views.CreateTicketView.as_view(),name="createTicket"),
    path("myTickets/",views.MyTicketsView.as_view(),name="myTickets"),
    path("myAll/",views.MyAllCategoryeis.as_view(),name="myAll"),
    path("saved/",views.SavedCategory.as_view(),name="saved"),
    path("myorders/",views.MyOrders.as_view(),name="myorders"),
    path("myprofile/",views.MyProfileView.as_view(),name="myprofile"),
    path("makeOrderFree/<str:id>/",views.MakeFreeOrder.as_view(),name="makeOrderFree"),
    path("msg/<str:id>/",views.CreateMessageView.as_view(),name="msg"),
    path("payProducts/<str:id>/",views.PayProducts.as_view(),name="payProducts"),
]