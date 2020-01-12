"""
Forms file
"""
from dal import autocomplete
from django import forms
from django.utils.translation import ugettext_lazy as _
from substitute.models import Category


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


NUTRI_CHOICES = (
    ("a", "A"),
    ("b", "B"),
    ("c", "C"),
    ("d", "D"),
    ("e", "E"),
)


class SearchForm(forms.Form):
    """
    Search substitute form
    """
    category = forms.ModelChoiceField(
        label="",
        queryset=Category.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(
            url='category-autocomplete',
            attrs={
                'class': 'mt-4',
                'data-placeholder': _('Categorie'),
                'onchange': 'search_form.submit();'}
        )
    )
    nutriscore = forms.ChoiceField(
        choices=NUTRI_CHOICES,
        label="",
        required=False,
        widget=forms.Select(
            attrs={
                'placeholder': _('Nutriscore'),
                'style': 'width:100%', 'class': 'form-group mt-4', 'onchange': 'search_form.submit();'
            }
        )
    )
    searching = forms.CharField(
        label="",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'mt-4', 'placeholder': _('search a substitute'),
                                      'title': _("search a substitute")})
    )



class SubstituteRegisterForm(forms.Form):
    """
    substitute register form
    """
    come_from = forms.CharField(max_length=100)
    searching_s = forms.CharField(max_length=100, required=False)
    category = forms.CharField(max_length=100, required=False)
    nutriscore = forms.CharField(max_length=100, required=False)
    user_id = forms.IntegerField()
    article_id = forms.IntegerField()
