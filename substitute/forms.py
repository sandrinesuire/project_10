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
    Search form
    """
    category = forms.ModelChoiceField(
        label=_("Categorie"),
        queryset=Category.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='category-autocomplete', attrs={'onchange': 'search_form.submit();'})
    )
    nutriscore = forms.ChoiceField(
        choices=NUTRI_CHOICES,
        label=_("Nutriscore"),
        required=False,
        widget=forms.Select(attrs={'style': 'width:100%', 'class': 'form-group', 'onchange': 'search_form.submit();'})
    )
    searching = forms.CharField(
        label=_("search a substitute"),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('search'),
                                      'title': _("search a substitute")})
    )


class SubstituteRegisterForm(forms.Form):
    """
    substitute register form
    """
    come_from = forms.CharField(max_length=100)
    searching = forms.CharField(max_length=100)
    user_id = forms.IntegerField()
    article_id = forms.IntegerField()
