from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth

from article.models import Article, UserProfile
from accounts.forms import *

def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            tmp_user = User.objects.create_user(username=form.cleaned_data.get('username'),
                                            password=form.cleaned_data.get('password1'),
                                            email=form.cleaned_data.get('email'),
                                            first_name=form.cleaned_data.get('first_name'),
                                            last_name=form.cleaned_data.get('last_name'),
                                            )
            user = UserProfile.objects.create(user=tmp_user, profile_photo=request.FILES['profile_photo'])
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
    user_with_photo = get_object_or_404(UserProfile, user=request.user)
    user = request.user

    articles = Article.objects.filter(author_id=user.id).order_by('-date')[:3]

    list_of_data = []
    for article in articles:
        num_votes = 0

        tmp = (article, article.comment_set.count(), 0)
        list_of_data.append(tmp)

    context = {
        'user_with_photo': user_with_photo,
        'list_of_data': list_of_data,
    }

    return render(request, 'accounts/profile_detail.html', context=context)


def profile_all_articles(request):
    user = request.user
    articles = Article.objects.filter(author=user).order_by('-date')

    list_of_data = []
    for article in articles:
        num_votes = 0

        tmp = (article, article.comment_set.count(), 0)
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
            user.set_password(form.cleaned_data.get('password1'))
            user.save()

            edited_user = auth.authenticate(username=form.cleaned_data.get('username'),
                                     password=form.cleaned_data.get('password'))
            auth.login(request, edited_user)

            return redirect('accounts:profile_detail')
    else:
        form = EditForm()

    context = {'form': form}

    return render(request, 'accounts/profile_edit.html', context)