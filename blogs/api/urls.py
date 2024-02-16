from django.urls import path,include
from . import views

urlpatterns=[
    path("",views.HomeViewBlogs.as_view(),name="blog-home"),
    path("each/<str:id>/",views.EachBlog.as_view(),name="each-blog"),
]