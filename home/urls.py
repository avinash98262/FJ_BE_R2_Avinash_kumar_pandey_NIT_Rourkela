
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home , name="home"),
    path('login_page/', login_page , name="login_page"),
    path('register_page/', register_page , name="register_page"),
   
]