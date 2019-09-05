"""
Views
"""

from django import shortcuts
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as _logout, authenticate, login
from django.urls import reverse
from django.utils import http

from substitute.forms import UserForm, LoginForm, SearchForm
from substitute.models import Profile, Article


def log_in(request):
    """
    Views for login
    :param request:
    :return:
    """
    form = LoginForm(request.POST or None)
    form_url = "log_in"
    redirect_to = request.POST.get('next', request.GET.get('next', '/'))
    redirect_to = (redirect_to
                   if http.is_safe_url(redirect_to, request.get_host())
                   else '/')
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return shortcuts.redirect(redirect_to)
            else:
                messages.error(request, 'username or password not correct')
                return redirect(log_in)
        else:
            messages.error(request, 'formulaire invalid')
            return redirect(log_in)

    return render(request, 'substitute/register.html', {'form': form,
                                                        'form_url': form_url,
                                                        'redirect_to': redirect_to})


def register(request, redirect_to='/'):
    """
    View for registring a new account
    :param request:
    :param redirect_to: when anonymous user click on link (needed login), he is redirect to login, he could call the
    registration url. Redirect_to memorise the link clicked at first by anonymous to redirect him at the good place
    :return:
    """
    form = UserForm(request.POST or None)
    form_url = "register"
    if form.is_valid():
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        try:
            user = User.objects.create_user(username, email, password)
        except:
            messages.error(request, 'Impossible to create user with these data')
            return redirect(register)
        profile = Profile.objects.create(user=user)
        if profile:  # Si l'objet renvoyé n'est pas None
            login(request, user)  # nous connectons l'utilisateur
            return shortcuts.redirect(redirect_to)
        else:
            messages.error(request, 'Impossible to create user with these data')
            return redirect(register)
    return render(request, 'substitute/register.html', {'form': form,
                                                        'form_url': form_url,
                                                        'redirect_to': '/'})


def logout(request):
    """
    View for logout
    :param request:
    :return:
    """
    _logout(request)
    return redirect(reverse(search))


def search(request):
    """
    View for searching a substitute
    :param request:
    :return: HttpResponse with message
    """
    form = SearchForm(request.POST or None)
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            chercher = form.cleaned_data["chercher"]
            result = Article.objects.filter(product_name__contains=chercher)
            if result.count() > 0:
                searched_article = result[0]
                articles = searched_article.get_article_substitutes_from_bd()
                print(articles)
                # return only the first twelve articles
                if len(articles) > 12:
                    articles = articles[:12]
                return render(request, 'substitute/results.html', {'searched_article': searched_article,
                                                                   'articles': articles,
                                                                   'backgrd': searched_article.image_url})

    return render(request, 'substitute/search.html', {'form': form})


def detail(request, article_id):
    """
    view for display article détail
    :param request:
    :param article_id: the article id
    :return:
    """
    article = Article.objects.get(pk=article_id)
    context = {
        'stores': article.stores,
        'code': article.code,
        'nutrition_grades': article.nutrition_grades,
        'product_name': article.product_name,
        'image_url': article.image_url,
        'nutriments': article.nutriments,
        'url': article.url,
        'ingredients': article.ingredients,
        'backgrd': article.image_url
    }
    return render(request, 'substitute/detail.html', context)


@login_required
def account(request):
    """
    Account view
    :param request:
    :return: HttpResponse with message
    """
    return render(request, 'substitute/account.html')


def legal(request):
    """
    Legal view
    :param request:
    :return: HttpResponse with message
    """
    return render(request, 'substitute/legal.html')

@login_required
def mysubstitutes(request):
    """
    Mysubstitutes view
    :param request:
    :return: HttpResponse with message
    """
    return render(request, 'substitute/mysubstitutes.html')
