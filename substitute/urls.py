"""
Urls
"""
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^searching$', views.search, name='search'),
    url(r'^(?P<article_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^register_substitut$', views.register_substitut, name='register_substitut'),
    url(r'^account$', views.account, name='account'),
    url(r'^legal$', views.legal, name='legal'),
    url(r'^results', views.results, name='results'),
    url(r'^mysubstitutes', views.mysubstitutes, name='mysubstitutes'),
    url(r'^category-autocomplete/$',
        views.CategoryAutocomplete.as_view(), name='category-autocomplete', ),
]
