"""
Views
"""

# from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as _logout
from django.urls import reverse


class MyForm(forms.Form):  # Note that it is not inheriting from forms.ModelForm
    chercher = forms.CharField(max_length=20)
    # All my attributes here


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
