"""
Views
"""

from django import forms, shortcuts
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as _logout, authenticate, login
from django.urls import reverse
from django.utils import http

from substitute.forms import UserForm, LoginForm
from substitute.models import Profil


class MyForm(forms.Form):  # Note that it is not inheriting from forms.ModelForm
    chercher = forms.CharField(max_length=20)
    # All my attributes here


def log_in(request):
    form = LoginForm(request.POST or None)
    form_url = "log_in"
    redirect_to = request.POST.get('next', request.GET.get('next', '/'))
    redirect_to = (redirect_to
                   if http.is_safe_url(redirect_to, request.get_host())
                   else '/')
    print(redirect_to)
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return shortcuts.redirect(redirect_to)
    return render(request, 'substitute/register.html', {'form': form,
                                                        'form_url': form_url,
                                                        'next': redirect_to})


def register(request, next='/'):
    form = UserForm(request.POST or None)
    form_url = "register"
    if form.is_valid():
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = User.objects.create_user(username, email, password)
        profil = Profil.objects.create(user=user)
        if profil:  # Si l'objet renvoyé n'est pas None
            login(request, user)  # nous connectons l'utilisateur
            return shortcuts.redirect(next)
    return render(request, 'substitute/register.html', {'form': form,
                                                        'form_url': form_url,
                                                        'next': '/'})


def logout(request):
    _logout(request)
    return redirect(reverse(search))


def search(request):
    """
    Index view
    :param request:
    :return: HttpResponse with message
    """
    form = MyForm()
    if request.method == 'POST':
        print("sdvdv")
        chercher = request.POST.get('chercher')
        print(chercher)

    template = loader.get_template('substitute/search.html')
    return HttpResponse(template.render(request=request))


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
