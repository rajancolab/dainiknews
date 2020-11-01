from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('articles/<str:slug>/', article_detail, name='article_detail_url'),

]