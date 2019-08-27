"""
Forms file
"""

from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    email = forms.CharField(max_length=100, label="Email")
    password = forms.CharField(max_length=100, label="Mot de passe")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    # email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, label="Mot de passe")


