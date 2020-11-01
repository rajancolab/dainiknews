from django.shortcuts import redirect


def redirect_articles(request):
    return redirect('index')