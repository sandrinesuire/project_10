"""
Views
"""

from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as _logout, authenticate, login
from django.urls import reverse
from newrelic import agent

from substitute.forms import UserForm, LoginForm, SearchForm, SubstituteRegisterForm
from substitute.models import Profile, Article, ProfileSubstitute


def cust_login_required(func):
    """
    decorator using to force the login and redirect to the initiale request
    :param func:
    :return:
    """
    def func_wrapper(request):
        """
        wrapper of decorator
        :param request:
        :return:
        """
        try:
            if not request.session.get('unlogged', "") and not request.session.get('old_request'):
                request.session['old_request'] = request.POST
            if isinstance(request.user, AnonymousUser):
                if not request.session.get('unlogged', ""):
                    request.session['unlogged'] = "second"
                    request.method = None
                    return log_in(request)
                elif request.session.get('unlogged', "") == "second" and 'register' in request.POST.get('form_url', ""):
                    return log_in(request)
                elif request.session.get('unlogged', "") == "third" or (request.session.get(
                        'unlogged', "") == "second" and 'log_in' in request.POST.get('form_url', "")):
                    log_in(request)
            request.POST = request.session.get('old_request')
            if request.session.get('old_request'):
                request.session['old_request'] = None
            if request.session.get('unlogged'):
                request.session['unlogged'] = None
        except:
            if request.session.get('old_request'):
                request.session['old_request'] = None
            if request.session.get('unlogged'):
                request.session['unlogged'] = None
            return redirect(log_in)
        return func(request)
    return func_wrapper


def log_in(request):
    """
    Views for login
    :param request:
    :return:
    """
    if request.method == "POST" and 'register' in request.POST.get('form_url', ""):
        form = UserForm(request.POST or None)
        form_url = "register"
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                user = User.objects.create_user(username, email, password)
            except IntegrityError:
                messages.error(request, _('Impossible to create user with these data'))
                return redirect(log_in)
            profile = Profile.objects.create(user=user)
            if profile:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                if request.session.get('unlogged'):
                    request.session['unlogged'] = None
                if request.session.get('old_request'):
                    request.session['old_request']['user_id'] = user.id
                else:
                    return redirect(search)
            else:
                messages.error(request, _('Impossible to create user with these data'))
                return redirect(log_in)
        elif request.session.get('unlogged', '') == "second":
            request.session['unlogged'] = "third"
            return render(request, 'substitute/register.html', {'form': form, 'form_url': form_url})
        elif not request.session.get('unlogged'):
            return render(request, 'substitute/register.html', {'form': form, 'form_url': form_url})
    else:
        form = LoginForm(request.POST or None)
        form_url = "log_in"
        if request.method == "POST":
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user:  # Si l'objet renvoyé n'est pas None
                    login(request, user)  # nous connectons l'utilisateur
                    if request.session.get('unlogged'):
                        request.session['unlogged'] = None
                    if request.session.get('old_request'):
                        request.session['old_request']['user_id'] = user.id
                    else:
                        return redirect(search)
                else:
                    messages.error(request, _('Impossible to create user with these data'))
                    return redirect(log_in)
            elif request.session.get('unlogged', '') == "second":
                return render(request, 'substitute/register.html', {'form': form, 'form_url': form_url})
        else:
            return render(request, 'substitute/register.html', {'form': form, 'form_url': form_url})


def logout(request):
    """
    View for logout
    :param request:
    :return:
    """
    request.session['unlogged'] = None
    _logout(request)
    return redirect(reverse(search))


def search(request):
    """
    View for search a substitute
    :param request:
    :return: HttpResponse with message
    """
    form = SearchForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        searching = form.cleaned_data["searching"]
        context = _search(searching)
        return render(request, 'substitute/results.html', context)

    return render(request, 'substitute/search.html', {'form': form})


def _search(searching):
    """
    Method private for search article in database
    :param searching: the searching name
    :return: the context for searching view
    """
    first = searching
    second = ' ' + searching + ' '
    third = ' ' + searching
    fourth = searching + '.'
    fifth = searching + ' '
    sixth = ' ' + searching
    results = Article.objects.filter(product_name__icontains=first)
    initial_search = ""
    if not results:
        results = Article.objects.filter(Q(product_name__contains=second) | Q(product_name__contains=third) |
                                        Q(product_name__istartswith=fourth) | Q(product_name__istartswith=fifth) |
                                        Q(product_name__iendswith=sixth))
    for result in results:
        initial_search += result.product_name + ", "
    content_title = _("No article can substitute your search.")
    if results.count() > 0:
        searched_article = results[0]
        image_url = searched_article.image_url
        articles = searched_article.get_article_substitutes_from_bd()
        if not articles:
            articles = results[1:]
        # return only the first twelve articles
        if articles:
            content_title = _("You can substitute this product with : ")
            if len(articles) > 12:
                articles = articles[:12]
            articles.sort(key=lambda x: [x.my_grade, x.ingredients_number, x.keywords_number],
                          reverse=True)
        masthead_content = searched_article.product_name
    else:
        searched_article = None
        articles = None
        content_title = _("This article not exist.")
        masthead_content = searching
        image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSP8Afx0GJ_ZY2djs-fT3zfLRIZHMq" \
                    "twBvkuRWej2Up8zYxgFx-"
    return {
        'searched_article': searched_article,
        'articles': articles,
        'masthead_content': masthead_content,
        'image_url': image_url,
        'content_title': content_title,
        'initial_search': initial_search
    }


def results(request):
    """
    View for results of search
    :param request:
    :return: HttpResponse with message
    """
    context = {}
    if request.method == "POST":
        form = SubstituteRegisterForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data["user_id"]
            searching = form.cleaned_data["searching"]
            article_id = form.cleaned_data["article_id"]
            profile = get_object_or_404(Profile, user__id=user_id)
            article = get_object_or_404(Article, id=article_id)
            ProfileSubstitute.objects.get_or_create(profile=profile, article=article)
            context = _search(searching)
            context["message"] = 'Your substitute has been registred successfully!'
    return render(request, 'substitute/results.html', context)


def detail(request, article_id):
    """
    view for display article détail
    :param request:
    :param article_id: the article id
    :return:
    """
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'stores': article.stores.all(),
        'code': article.code,
        'nutrition_grades': article.nutrition_grades,
        'masthead_content': article.product_name,
        'searched_article': article,
        'image_url': article.image_url,
        'nutriments': article.nutriments,
        'url': article.url,
        'ingredients': article.ingredients,
        'content_title': _("Here is the detailed card of your product")
    }
    if request.method == "POST":
        form = SubstituteRegisterForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data["user_id"]
            article_id = form.cleaned_data["article_id"]
            profile = get_object_or_404(Profile, user__id=user_id)
            article = get_object_or_404(Article, id=article_id)
            ProfileSubstitute.objects.get_or_create(profile=profile, article=article)
            context["message"] = _('Your substitute has been registred successfully!')
    return render(request, 'substitute/detail.html', context)


@cust_login_required
def register_substitut(request):
    """
    view for display article détail
    :param request:
    :return:
    """
    if request.method == "POST":
        form = SubstituteRegisterForm(request.POST)
        if form.is_valid():
            come_from = form.cleaned_data["come_from"]
            user_id = form.cleaned_data["user_id"]
            searching = form.cleaned_data["searching"]
            article_id = form.cleaned_data["article_id"]
            profile = get_object_or_404(Profile, user__id=user_id)
            article = get_object_or_404(Article, id=article_id)
            ProfileSubstitute.objects.get_or_create(profile=profile, article=article)

            if come_from == "results":
                context = _search(searching)

            elif come_from == "detail":
                context = {
                    'stores': article.stores.all(),
                    'code': article.code,
                    'nutrition_grades': article.nutrition_grades,
                    'masthead_content': article.product_name,
                    'searched_article': article,
                    'image_url': article.image_url,
                    'nutriments': article.nutriments,
                    'url': article.url,
                    'ingredients': article.ingredients,
                    'content_title': _("Here is the detailed card of your product")
                }
            else:
                context = {}
            print("test log ", user_id)
            agent.add_custom_parameter('user_id', user_id)

            context["message"] = _('Your substitute has been registred successfully!')
            return render(request, 'substitute/' + come_from + '.html', context)
    return redirect(log_in)

@cust_login_required
def account(request):
    """
    Account view
    :param request:
    :return: HttpResponse with message
    """
    context = {'local_background': 'user',
               'masthead_content': request.user.username,
               'content_title': _("Here is your user profile :")
               }
    return render(request, 'substitute/account.html', context)


def legal(request):
    """
    Legal view
    :param request:
    :return: HttpResponse with message
    """
    context = {
        "content_title": _("Legality : ")
    }
    return render(request, 'substitute/legal.html', context)


@cust_login_required
def mysubstitutes(request):
    """
    Mysubstitutes view
    :param request:
    :return: HttpResponse with message
    """
    substitutes = ProfileSubstitute.objects.filter(profile__user=request.user)
    if substitutes:
        content_title = _("Here is the list of your substitutes :")
    else:
        content_title = _("You do not have a registered substitute yet")
    context = {
        'local_background': 'mysubstitutes',
        'substitutes': substitutes,
        'masthead_content': _("My substitutes"),
        'content_title': content_title
    }
    return render(request, 'substitute/mysubstitutes.html', context)
