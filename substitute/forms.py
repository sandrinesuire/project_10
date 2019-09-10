"""
Forms file
"""

from django import forms


class UserForm(forms.Form):
    """
    User form used for registration
    """
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    email = forms.CharField(max_length=100, label="Email")
    password = forms.CharField(max_length=100, label="Mot de passe")


class LoginForm(forms.Form):
    """
    Login form used for login
    """
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    password = forms.CharField(max_length=100, label="Mot de passe")


class SearchForm(forms.Form):
    """
    Search form
    """
    search = forms.CharField(max_length=100)


class SubstituteRegisterForm(forms.Form):
    """
    substitute register form
    """
    search = forms.CharField(max_length=100)
    user_id = forms.IntegerField()
    article_id = forms.IntegerField()
