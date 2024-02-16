from django.urls import path,include
from . import views

urlpatterns=[
    path("free/",views.MainFreeCatsReview.as_view(),name="free-reviews"),
    path("addFree/",views.MakeFreeReviewMainPage.as_view(),name="addFree-reviews"),
    path("addFree/<str:id>/",views.MakeFreeReviewEachPackage.as_view(),name="addFree-reviews"),
    path("free/<str:id>/",views.EachFreeCatReview.as_view(),name="each-free-reviews"),
    path("eachBlog/<str:id>/",views.EachBlocgComments.as_view(),name="eachBlog"),
    
]