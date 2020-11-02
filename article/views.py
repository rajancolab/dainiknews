from django.http import Http404
from django.shortcuts import render, redirect

from .models import Article, Comment
from .forms import CreateArticleForm


def index(request):

    articles = Article.objects.order_by('-data')

    list_of_data = []
    for article in articles:
        num_votes = 0
        for choice in article.choice_set.all():
            num_votes += choice.votes
        tmp = (article, article.comment_set.count(), num_votes)
        list_of_data.append(tmp)

    context = {
        'list_of_data': list_of_data,
    }
    return render(request, 'article/index.html', context=context)


def article_detail(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except:
        raise Http404("Article not found!")
    comments = article.comment_set.all()
    choices = article.choice_set.all()

    return render(request, 'article/article_detail.html', {'article': article, 'comments': comments, 'choices': choices})


def create_article(request):

    if request.method == "POST":
        form = CreateArticleForm(request.POST)

        if form.is_valid():
            article = Article.objects.create(title=request.POST['title'], text=request.POST['text'], author=request.user)
            article.save()
            return redirect('article_detail_url', article.slug)

    else:
        form  = CreateArticleForm()

    context = {'form': form}

    return render(request, 'article/article_create.html', context)


def vote(request, slug):
    try:
        article = Article.objects.get(slug=slug)
        choice_text = request.POST['choiceText']
        choice = article.choice_set.get(text=choice_text)
        choice.votes += 1
        choice.save()
        return redirect('article_detail_url', slug)
    except:
        raise Http404("Article not found!")



def comment(request, slug):
    try:
        article = Article.objects.get(slug=slug)
        comment_text = request.POST['commentText']
    except:
        raise Http404("Article not found!")
    comment = Comment.objects.create(article=article, text=comment_text, author=request.user)
    comment.save()
    return redirect('article_detail_url', slug)
