from django.urls import path
from . import view

urlpatterns=[
    path("",view.Home.as_view(),name="home-cats"),
    path("allPackage/",view.AllPayPackage.as_view(),name="allPackage"),
    path("free/",view.FreeCats.as_view(),name="free-cats"),
    path("each/<str:id>/",view.EachCategory.as_view(),name="each-category"),
    path("save/<str:id>/",view.save_cat,name="save-category"),
    path("package/<str:id>/",view.EachPayPackage.as_view(),name="each-package"),
    path("freePackage/<str:id>/",view.EachFreePackage.as_view(),name="free-package"),
]