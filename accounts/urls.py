from django.urls import path
from .views import *


app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register_url'),
    path('login/', login, name='login_url'),
    path('logout/', logout, name='logout_url')
]