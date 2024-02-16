from django.urls import path,include
from . import views

urlpatterns=[
    path("loginReg/",views.UserRegisterOrLogin.as_view(),name="loginOrReg"),
    path("login/",views.Login.as_view(),name="login"),
]