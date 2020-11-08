from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
        tmp = (article, article.comment_set.count(), article.likes + article.dislikes)
        list_of_data.append(tmp)

    paginator = Paginator(list_of_data, 12)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''


    context = {
        # 'list_of_data': list_of_data,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
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


@login_required
def create_article(request):

    if request.method == "POST":
        form = CreateArticleForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            article = Article.objects.create(
                title=request.POST['title'],
                text=request.POST['text'],
                author=request.user,
                image=request.FILES['image'] if request.FILES else ''
            )
            article.save()
            return redirect('article_detail_url', article.slug)

        else:
            messages.error(request, ('Please correct the error below.'))



    else:
        form = CreateArticleForm()

    context = {'form': form}

    return render(request, 'article/article_create.html', context)


@login_required
def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    print(article)

    if article.author != request.user:
        raise PermissionDenied

    if request.method == "POST":
        form = EditArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.date = datetime.now()
            article.image = request.FILES['image']
            article.save()
            messages.success(request, ('Your article was successfully updated!'))
            return redirect('article_detail_url', article.slug)
    else:
        form = EditArticleForm({'title': article.title, 'text': article.text, 'image': article.image})

    context = {'form': form,
               'slug': slug}

    return render(request, 'article/article_edit.html', context)


@login_required
def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if article.author != request.user:
        raise PermissionDenied

    if request.method == "POST":
        article.delete()
        return redirect('accounts:profile_detail')

    context = {
        'slug': slug,
        'article': article
    }
    return render(request, 'article/article_delete.html', context)


@login_required
def like_dislike_article(request, slug):

    article = get_object_or_404(Article, slug=slug)

    if 'like' in request.POST:
        article.likes += 1
        article.save()
        return redirect('article_detail_url', slug)

    elif 'dislike' in request.POST:
        article.dislikes += 1
        article.save()
        return redirect('article_detail_url', slug)


@login_required
def comment(request, slug):

    article = get_object_or_404(Article, slug=slug)
    comment_text = request.POST['commentText']
    new_comment = Comment.objects.create(article=article, text=comment_text, author=request.user)
    new_comment.save()
    return redirect('article_detail_url', slug)
