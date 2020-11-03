from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('create_article/', create_article, name='create_article'),
    # path('<str:slug>/vote/', vote, name='vote_url'),
    path('<str:slug>/comment/', comment, name='comment_url'),
    path('<str:slug>/edit/', edit_article, name='article_edit_url'),
    path('<str:slug>/delete/', delete_article, name='article_delete_url'),
    path('<str:slug>/like/', like_dislike_article, name='article_like_url'),
    path('<str:slug>/', article_detail, name='article_detail_url'),
]