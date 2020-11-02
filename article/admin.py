from django.contrib import admin

from article.models import Article, Comment, Choice




admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Choice)
