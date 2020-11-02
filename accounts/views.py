from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

from article.models import Article
from accounts.forms import *

def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data.get('username'),
                                            password=form.cleaned_data.get('password1'),
                                            email=form.cleaned_data.get('email'),
                                            first_name=form.cleaned_data.get('first_name'),
                                            last_name=form.cleaned_data.get('last_name')
                                            )
            user.save()
            return redirect('accounts:login_url')
    else:
        form = RegisterForm()

    context = {'form': form}

    return render(request, 'accounts/profile_register.html', context)



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('username'),
                                     password=form.cleaned_data.get('password'))
            auth.login(request, user)
            return redirect('accounts:profile_detail')
    else:
        form = LoginForm()

    context = {'form': form}

    return render(request, 'accounts/profile_login.html', context)




def logout(request):
    auth.logout(request)
    return redirect('/')


def profile_detail(request):
    user = request.user
    articles = Article.objects.filter(author=user).order_by('-data')[:3]

    list_of_data = []
    for article in articles:
        num_votes = 0
        for choice in article.choice_set.all():
            num_votes += choice.votes
        tmp = (article, article.comment_set.count(), num_votes)
        list_of_data.append(tmp)

    context = {
        'user': user,
        'list_of_data': list_of_data,
    }

    return render(request, 'accounts/profile_detail.html', context=context)


def profile_all_articles(request):
    user = request.user
    articles = Article.objects.filter(author=user).order_by('-data')

    list_of_data = []
    for article in articles:
        num_votes = 0
        for choice in article.choice_set.all():
            num_votes += choice.votes
        tmp = (article, article.comment_set.count(), num_votes)
        list_of_data.append(tmp)

    context = {
        'user': user,
        'list_of_data': list_of_data,
    }

    return render(request, 'accounts/profile_all_articles.html', context=context)

def profile_edit(request):
    if request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.username = form.cleaned_data.get('username')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            print(user.password)
            user.set_password = form.cleaned_data.get('password1')
            print(user.password)


            user.save()
            return redirect('accounts:profile_detail')
    else:
        form = EditForm()

    context = {'form': form}

    return render(request, 'accounts/profile_edit.html', context)