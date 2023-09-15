
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home , name="home"),
    path('accounts/login/', login_page, name="login_page"),
    path('accounts/register/', register_page, name="register_page"),
    path('edit_expense/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('delete_expense/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('logout/', logout_user, name='logout_user'),
   
]