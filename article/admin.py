from django.contrib import admin

from article.models import Article, User, Comment, Choice




admin.site.register(Article)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Choice)
