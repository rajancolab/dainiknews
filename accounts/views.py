# from importlib._common import _

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth

from article.models import Article
from accounts.forms import *


def register(request):

    if request.method == "POST":
        print(request.FILES)
        user_form = RegisterUserForm(request.POST)
        profile_form = RegisterProfileForm(request.POST, request.FILES)
        print(user_form.is_valid())
        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.create_user(username=user_form.cleaned_data.get('username'),
                                            first_name=user_form.cleaned_data.get('first_name'),
                                            last_name=user_form.cleaned_data.get('last_name'),
                                            password=user_form.cleaned_data.get('password1'),
                                            email=user_form.cleaned_data.get('email'),
                                            )
            user.profile.photo = profile_form.cleaned_data.get('photo')
            user.profile.bio = profile_form.cleaned_data.get('bio')
            user.save()
            messages.success(request, ('Successful registration! Welcome to the DanikSNews! '))
            return redirect('accounts:login_url')
        else:
            pass
            # messages.error(request, ('Please correct the error below.'))
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
        tmp = (article, article.comment_set.count(), article.likes+article.dislikes)
        list_of_data.append(tmp)

    paginator = Paginator(list_of_data, 5)

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
        'user': user,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'accounts/profile_all_articles.html', context=context)


@login_required
def edit_profile(request):

    if request.method == "POST":

        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm( request.POST, request.FILES, instance=request.user.profile)

        print(user_form.is_valid())

        if user_form.is_valid() and profile_form.is_valid():

            # if not request.user.check_password(user_form.cleaned_data.get('password0')):
            #     raise forms.ValidationError('Previous password is not correct')

            # request.user.set_password(user_form.cleaned_data.get('password'))
            password_for_login = request.user.password
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))

            user = auth.authenticate(username=user_form.cleaned_data.get('username'),
                                     password=password_for_login,
                                     )

            auth.login(request, user)

            return redirect('accounts:profile_detail')

        else:
            pass
            # messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def change_password_profile(request):

    if request.method == "POST":

        password_form = ChangePasswordUserForm(request.POST, instance=request.user)

        if password_form.is_valid():

            if not request.user.check_password(password_form.cleaned_data.get('password0')):
                messages.error(request, 'Previous password is not correct!')
                return render(request, 'accounts/profile_change_password.html', {'password_form': password_form})

            request.user.set_password(password_form.cleaned_data.get('password1'))
            username_for_login = request.user.username
            password_form.save()
            messages.success(request, ('Your password was successfully updated!'))

            user = auth.authenticate(username=username_for_login, password=password_form.cleaned_data.get('password1'))
            auth.login(request, user)

            return redirect('accounts:profile_detail')

        else:
            pass
            # messages.error(request, ('Please correct the error below.'))
    else:
        password_form = ChangePasswordUserForm(instance=request.user)

    return render(request, 'accounts/profile_change_password.html', {'password_form': password_form})

