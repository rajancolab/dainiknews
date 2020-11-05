from django.urls import path
from .views import *


app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register_url'),
    path('login/', login, name='login_url'),
    path('logout/', logout, name='logout_url'),
    path('profile/', profile_detail, name='profile_detail'),
    path('profile/articles/', profile_all_articles, name='profile_all_articles'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change_password/', change_password_profile, name='change_password_profile'),

]