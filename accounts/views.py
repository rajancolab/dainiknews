# from importlib._common import _

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth

from article.models import Article
from accounts.forms import *


def register(request):

    if request.method == "POST":
        user_form = RegisterUserForm(request.POST)
        profile_form = RegisterProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.create_user(username=user_form.cleaned_data.get('username'),
                                            first_name=user_form.cleaned_data.get('first_name'),
                                            last_name=user_form.cleaned_data.get('last_name'),
                                            password=user_form.cleaned_data.get('password'),
                                            email=user_form.cleaned_data.get('email'),
                                            )
            user.profile.photo = profile_form.cleaned_data.get('photo')
            user.profile.bio = profile_form.cleaned_data.get('bio')
            user.save()
            messages.success(request, ('Successful registration! Welcome to the DanikSNews! '))
            return redirect('accounts:login_url')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = RegisterUserForm()
        profile_form = RegisterProfileForm()

    return render(request, 'accounts/profile_register.html', context={
        'user_form': user_form,
        'profile_form': profile_form
    })


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


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')



@login_required
def profile_detail(request):
    user = request.user

    articles = Article.objects.filter(author_id=user.id).order_by('-date')[:3]

    list_of_data = []
    for article in articles:
        num_votes = 0

        tmp = (article, article.comment_set.count(), 0)
        list_of_data.append(tmp)

    context = {
        'user': user,
        'list_of_data': list_of_data,
    }

    return render(request, 'accounts/profile_detail.html', context=context)

@login_required
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


@login_required
def edit_profile(request):

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm( request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():

            request.user.set_password(user_form.cleaned_data.get('password'))
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))

            user = auth.authenticate(username=user_form.cleaned_data.get('username'),
                                     password=user_form.cleaned_data.get('password'))
            auth.login(request, user)

            return redirect('accounts:profile_detail')

        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

