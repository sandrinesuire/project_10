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

from substitute.forms import UserForm, LoginForm, SearchForm, SubstituteRegisterForm
from substitute.models import Profile, Article, ProfileSubstitute


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
    if request.method == "POST" and form.is_valid():
        search = form.cleaned_data["search"]
        context = _search(search)
        return render(request, 'substitute/results.html', context)

    return render(request, 'substitute/search.html', {'form': form})


def _search(search):
    """
    Method private for searching article in database
    :param search: the search name
    :return: the context for search view
    """
    result = Article.objects.filter(product_name__contains=search)
    if result.count() > 0:
        searched_article = result[0]
        backgrd = searched_article.image_url
        articles = searched_article.get_article_substitutes_from_bd()
        # return only the first twelve articles
        if articles and len(articles) > 12:
            articles = articles[:12]
    else:
        searched_article = None
        articles = None
        backgrd = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSP8Afx0GJ_ZY2djs-fT3zfLRIZHMq" \
                  "twBvkuRWej2Up8zYxgFx-"
    return {
        'searched_article': searched_article,
        'articles': articles,
        'search': search,
        'backgrd': backgrd
    }


def results(request):
    """
    View for results of search
    :param request:
    :return: HttpResponse with message
    """
    if request.method == "POST":
        form = SubstituteRegisterForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data["user_id"]
            search = form.cleaned_data["search"]
            article_id = form.cleaned_data["article_id"]
            profile = Profile.objects.get(user__id=user_id)
            article = Article.objects.get(id=article_id)
            profile_substitute = ProfileSubstitute.objects.get_or_create(profile=profile, article=article)
            context = _search(search)
            context["message"] = 'Your substitute has been registred successfully!'
            return render(request, 'substitute/results.html', context)


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
    context = {'local_background': 'user'}
    return render(request, 'substitute/account.html', context)


def legal(request):
    """
    Legal view
    :param request:
    :return: HttpResponse with message
    """

    return render(request, 'substitute/legal.html', )

@login_required
def mysubstitutes(request):
    """
    Mysubstitutes view
    :param request:
    :return: HttpResponse with message
    """
    substitutes = ProfileSubstitute.objects.filter(profile__user=request.user)
    context = {
        'local_background': 'mysubstitutes',
        'substitutes': substitutes
    }
    return render(request, 'substitute/mysubstitutes.html', context)
