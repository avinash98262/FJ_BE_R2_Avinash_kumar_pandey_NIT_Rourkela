
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home , name="home"),
    path('accounts/login/', login_page, name="login_page"),
    path('accounts/register/', register_page, name="register_page"),

   
]