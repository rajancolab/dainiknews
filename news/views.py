from django.shortcuts import redirect, render


def redirect_articles(request):
    return redirect('index')

def home(request):
    return render(request, 'home.html')