from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

from article.models import Article


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']


        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('accounts:register_url')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('accounts:register_url')
            else:
                user = User.objects.create_user(username=username,
                                                password=password1,
                                                email=email,
                                                first_name=first_name,
                                                last_name=last_name
                                                )
                user.save()
                return redirect('accounts:login_url')
        else:
            messages.info(request, 'Confirmation password failed')
            return redirect('accounts:register_url')


    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Данные введены неверно ')
            return redirect('accounts:login_url')

    else:
        return render(request, 'accounts/login.html')


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
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['second_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']


        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('accounts:register_url')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('accounts:register_url')
            else:
                user = User.objects.create_user(username=username,
                                                password=password1,
                                                email=email,
                                                first_name=first_name,
                                                last_name=last_name
                                                )
                user.save()
                return redirect('accounts:login_url')
        else:
            messages.info(request, 'Confirmation password failed')
            return redirect('accounts:register_url')


    else:
        return render(request, 'accounts/profile_edit.html')