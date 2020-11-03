from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.datetime_safe import datetime

from .models import Article, Comment
from .forms import *


def index(request):

    articles = Article.objects.order_by('-date')

    list_of_data = []
    for article in articles:
        num_votes = 0
        # for choice in article.choice_set.all():
        #     num_votes += choice.votes
        tmp = (article, article.comment_set.count(), article.likes + article.dislikes)
        list_of_data.append(tmp)

    context = {
        'list_of_data': list_of_data,
    }
    return render(request, 'article/index.html', context=context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comments': comments,
        'likes_percent' : article.likes*100/(article.likes+article.dislikes) if article.likes else 50,
        'dislikes_percent' : 100-article.likes*100/(article.likes+article.dislikes) if article.dislikes else 50,
    }

    return render(request, 'article/article_detail.html', context)


def create_article(request):

    if request.method == "POST":
        form = CreateArticleForm(request.POST)

        if form.is_valid():
            article = Article.objects.create(
                title=request.POST['title'],
                text=request.POST['text'],
                author=request.user)
            article.save()
            return redirect('article_detail_url', article.slug)

    else:
        form = CreateArticleForm()

    context = {'form': form}

    return render(request, 'article/article_create.html', context)


def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if article.author != request.user:
        raise PermissionDenied

    if request.method == "POST":
        form = EditArticleForm(request.POST)

        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.date = datetime.now()
            article.save()
            return redirect('article_detail_url', article.slug)
    else:
        form = EditArticleForm({'title': article.title, 'text': article.text})

    context = {'form': form,
               'slug': slug}

    return render(request, 'article/article_edit.html', context)


def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == "POST":
        article.delete()
        return redirect('accounts:profile_detail')

    context = {
        'slug': slug,
        'article': article
    }
    return render(request, 'article/article_delete.html', context)


def like_dislike_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    print('hereee')
    if 'like' in request.POST:
        article.likes += 1
        article.save()
        return redirect('article_detail_url', slug)
    elif 'dislike' in request.POST:
        article.dislikes += 1
        article.save()
        return redirect('article_detail_url', slug)


def comment(request, slug):

    article = get_object_or_404(Article, slug=slug)
    comment_text = request.POST['commentText']
    new_comment = Comment.objects.create(article=article, text=comment_text, author=request.user)
    new_comment.save()
    return redirect('article_detail_url', slug)
