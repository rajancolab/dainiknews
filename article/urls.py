from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<str:slug>/vote/', vote, name='vote_url'),
    path('<str:slug>/comment/', comment, name='comment_url'),
    path('<str:slug>/', article_detail, name='article_detail_url'),


]