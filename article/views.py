from django.http import Http404
from django.shortcuts import render, redirect
from .models import Article


def index(request):

    articles = Article.objects.order_by('-data')

    list_of_data = []
    for article in articles:
        tmp = (article, article.comment_set.count(), 0)
        list_of_data.append(tmp)

    context = {
        'list_of_data': list_of_data,
    }
    return render(request, 'article/index.html', context=context)


def article_detail(request, slug):

    if not request.method == 'post':
        try:
            article = Article.objects.get(slug=slug)
            comments = article.comment_set.all()
            choices = article.choice_set.all()
        except:
            raise Http404("Article not found!")
        return render(request, 'article/article_detail.html', {'article': article, 'comments': comments, 'choices': choices})
    # else:
    #     request.POST['']


